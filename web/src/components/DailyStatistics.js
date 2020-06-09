import React from 'react';
import {
    Container,
    Row,
    Col,
    Form,
    Spinner
} from 'react-bootstrap';

import { Line } from 'react-chartjs-2';

import {
    get_location,
    get_daily_statistics
} from '../services/API';

// eslint-disable-next-line
Date.prototype.addHours = function(h){
    this.setTime(this.getTime() + (h*60*60*1000));
    return this;
}

// eslint-disable-next-line
Date.prototype.getDateInputString = function(){
    let day = this.getDate();
    let month = this.getMonth()+1;
    let year = this.getFullYear();
    if(day < 10){
        day = "0"+ day;
    }
    if(month < 10){
        month = "0"+ (month);
    }
    return year + "-" + month + "-" + day;
}

// eslint-disable-next-line
Date.prototype.getDateTimeInputString = function(){
    let day = this.getDate();
    let month = this.getMonth()+1;
    let year = this.getFullYear();
    let hour = this.getHours();
    let minute = this.getMinutes();
    if(day < 10){
        day = "0"+ day;
    }
    if(month < 10){
        month = "0"+ (month);
    }
    if(hour < 10){
        hour = "0"+ (hour);
    }
    if(minute < 10){
        minute = "0"+ (minute);
    }
    return year + "-" + month + "-" + day + "T" + hour + ":" + minute;
}

function DailyStatistics() {
    let [ locationList, setLocationList ] = React.useState([]);

    let [ locationID, setLocationID] = React.useState("");
    let [ date, setDate ] = React.useState("");

    let [ showSpinner, setShowSpinner ] = React.useState(false);

    let [ displayList, setDisplayList ] = React.useState([]);
    let [ max , setMax ] = React.useState(0);
    let [ min , setMin ] = React.useState(0);
    let [ avg , setAvg ] = React.useState(0);

    React.useEffect(() => {
        function compareLocation(a, b){
            return a.id - b.id;
        }

        async function fetchData(){
            let location_response = await get_location();
            let temp = location_response.data;
            temp.sort(compareLocation);

            setLocationList(temp);
        }
        fetchData();
        let date_today = new Date();
        setDate(date_today.getDateInputString());
    }, []);

    React.useEffect(() => {
        if(locationList.length === undefined || locationList.length === 0){
            return;
        }
        setLocationID(locationList[0].id);
    },[locationList]);

    React.useEffect(() => {
        if(locationID === "" || date === ""){
            return;
        }
        
        async function fetchData(){
            setShowSpinner(true);
            let target_date = new Date(date);
            target_date.setHours(0);

            let statistic_response = await get_daily_statistics(locationID, target_date.getDateInputString());
            let temp = statistic_response.data;
            for(let i = 0; i < temp.length; i++){
                let time;
                if(i < 10){
                    time = "0" + i + "00";
                } else {
                    time = i + "00";
                }
                temp[i].time = time;
            }

            setDisplayList(temp);
            setShowSpinner(false);
        }
        
        fetchData();
    }, [date, locationID]);

    React.useEffect(() => {
        if(displayList === undefined || displayList.length === 0){
            setMax("-");
            setMin("-");
            setAvg("-");
            return;
        }

        let max = 0;
        let min = Number.MAX_VALUE;
        let total = 0;

        for(let i = 0; i < displayList.length; i++){
            if(displayList[i].max > max){
                max = displayList[i].max
            }
            if(displayList[i].min < min){
                min = displayList[i].min
            }
            total = total + displayList[i].average
        }
        setMax(max);
        setMin(min);
        setAvg(Math.ceil(total/displayList.length));
    }, [displayList]);

    return(
        <Container>
            <Row>
                <Col sm="12" lg="3" className="pt-3">
                    <h1>Statistics</h1>
                </Col>
            </Row>
            <Row>
                <Col sm="12" lg="3">
                    <Form.Group>
                        <Form.Label>Location:</Form.Label>
                        <Form.Control as="select" value={locationID} onChange={(e) => {setLocationID(e.target.value)}}>
                            {
                                locationList.map((l) => {
                                    return (
                            <option key={l.name + "_" + l.id} value={l.id}>{l.name}</option>
                                    )
                                })
                            }
                        </Form.Control>
                    </Form.Group>
                </Col>
                <Col sm="12" lg="3">
                    <Form.Group>
                        <Form.Label>Date:</Form.Label>
                        <Form.Control type="date" value={date} onChange={(e) => {setDate(e.target.value)}}></Form.Control>
                    </Form.Group>
                </Col>
                <Col className="d-flex align-items-end flex-column">
                    {
                        (showSpinner) ? (<Spinner as="span" animation="border" variant="primary"/>) : ("")
                    }
                </Col>
            </Row>
            <hr />
            <Row>
                <Col xs="4">
                    <h4>Max: {max}</h4>
                </Col>
                <Col xs="4">
                    <h4>Min: {min}</h4>
                </Col>
                <Col xs="4">
                    <h4>Avg: {avg}</h4>
                </Col>
            </Row>
            <hr />
            <Row>
                <Col>
                    <DailyCountChart
                        records={displayList} 
                    />
                </Col>
            </Row>
        </Container>
    );
}

function DailyCountChart(props) {
    let [ maxList , setMaxList ] = React.useState([]);
    let [ minList , setMinList ] = React.useState([]);
    let [ avgList , setAvgList ] = React.useState([]);
    let [ labels , setLabels ] = React.useState([]);

    let chartData = {
        data: {
           labels: labels,
           datasets: [
              {
                 data: maxList,
                 label: "Max",
                 fill: false,
                 lineTension: 0,
                 borderColor: "#EB2D3A",
                 pointRadius: 0
              },
              {
                 data: minList,
                 label: "Min",
                 fill: false,
                 lineTension: 0,
                 borderColor: "#08B46B",
                 pointRadius: 0
              },
              {
                 data: avgList,
                 label: "Average",
                 fill: false,
                 lineTension: 0,
                 borderColor: "#ADD8E6",
                 pointRadius: 0
              }
           ]
        },
        options: {
           animation: {
              duration: 1000, // general animation time
              easing: "easeOutBack"
           },
           hover: {
              animationDuration: 1000, // duration of animations when hovering an item
              mode: "label"
           },
           responsiveAnimationDuration: 1000, // animation duration after a resize
           responsive: true,
           maintainAspectRatio: false,
           scales: {
              xAxes: [
                 {
                    display: true,
                    gridLines: {
                       color: "#f3f3f3",
                       drawTicks: false
                    },
                    scaleLabel: {
                       display: true,
                       labelString: "Time"
                    },
                    ticks: {
                       padding: 10
                    }
                 }
              ],
              yAxes: [
                 {
                    display: true,
                    gridLines: {
                       color: "#f3f3f3",
                       drawTicks: false
                    },
                    scaleLabel: {
                       display: true,
                       labelString: "Number of People"
                    },
                    ticks: {
                       padding: 10,
                       precision: 0
                    }
                 }
              ]
           }
        }
     };

     React.useEffect(() => {
        let temp_max = [];
        let temp_min = [];
        let temp_avg = [];
        let temp_labels = [];
        
        for(let i = 0; i < props.records.length; i ++){
            temp_max.push(props.records[i].max);
            temp_min.push(props.records[i].min);
            temp_avg.push(props.records[i].average);
            temp_labels.push(props.records[i].time);
            // temp_labels.push("");
        }
        setMaxList(temp_max);
        setMinList(temp_min);
        setAvgList(temp_avg);
        setLabels(temp_labels);
    },[ props.records]);

    return(
        <Line
            data={chartData.data}
            options={chartData.options}
            height={500}
        />
    );
}

export default DailyStatistics;
