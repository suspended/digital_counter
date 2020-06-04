import React from 'react';
import {
    Container,
    Row,
    Col,
    Form,
    Button
} from 'react-bootstrap';

import { Line } from 'react-chartjs-2';

import {
    get_location,
    get_statistics
} from '../services/API';

// eslint-disable-next-line
Date.prototype.addHours = function(h){
    this.setTime(this.getTime() + (h*60*60*1000));
    return this;
}

// eslint-disable-next-line
Date.prototype.getInputString = function(){
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

function Statistics() {
    let [ locationList, setLocationList ] = React.useState([]);

    let [ locationID, setLocationID] = React.useState("");
    let [ startDate, setStartDate ] = React.useState("");
    let [ endDate, setEndDate ] = React.useState("");
    let [ numPoints, setNumPoints ] = React.useState(100);

    let [ recordList , setRecordList ] = React.useState([]);
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
        let date_start = new Date();
        let date_end = new Date();
        date_start = date_start.addHours(-1);
        setStartDate(date_start.getInputString());
        setEndDate(date_end.getInputString());
    }, []);

    React.useEffect(() => {
        if(locationList.length === undefined || locationList.length === 0){
            return;
        }
        setLocationID(locationList[0].id);
    },[locationList]);

    const onClickStatistics = async () => {
        function compareRecord(a, b){
            var date_a = new Date(a.time);
            var date_b = new Date(b.time);
            return date_a - date_b;
        }

        let statistic_response = await get_statistics(locationID, startDate, endDate);
        // sort response
        let temp = statistic_response.data.stats;
        temp.sort(compareRecord);
        for(let i = 0; i < temp.length; i ++){
            temp[i].time = (new Date(temp[i].time)).toLocaleString();
        }

        setRecordList(temp);
    }

    React.useEffect(() => {
        if(recordList === undefined || recordList.length === 0){
            setMax("-");
            setMin("-");
            setAvg("-");
            return;
        }
        let max = 0;
        let min = 999;
        let total = 0;
        for(let i = 0; i < recordList.length; i++){
            if(recordList[i].count > max){
                max = recordList[i].count
            }
            if(recordList[i].count < min){
                min = recordList[i].count
            }
            total = total + recordList[i].count
        }
        setMax(max);
        setMin(min);
        setAvg(Math.ceil(total/recordList.length));
    }, [recordList]);

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
                        <Form.Label>Start Date:</Form.Label>
                        <Form.Control type="datetime-local" step="60" value={startDate} onChange={(e) => {setStartDate(e.target.value)}}></Form.Control>
                    </Form.Group>
                </Col>
                <Col sm="12" lg="3">
                    <Form.Group>
                        <Form.Label>End Date:</Form.Label>
                        <Form.Control type="datetime-local" step="60" value={endDate} onChange={(e) => {setEndDate(e.target.value)}}></Form.Control>
                    </Form.Group>
                </Col>
                <Col sm="12" lg="3">
                    <Form.Group>
                        <Form.Label>Number of Points</Form.Label>
                        <Form.Control type="number" value={numPoints} onChange={(e) => {setNumPoints(e.target.value)}}></Form.Control>
                    </Form.Group>
                </Col>
            </Row>
            <Row>
                <Col className="d-flex align-items-end flex-column">
                    <Button className="mt-auto mb-3" onClick={() =>{onClickStatistics()}}>Get Statistics</Button>
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
                    <CountChart
                        records={recordList} 
                        numPoints={numPoints}
                    />
                </Col>
            </Row>
        </Container>
    );
}

function CountChart(props) {
    let [ data , setData ] = React.useState([]);
    let [ labels , setLabels ] = React.useState([]);

    let chartData = {
        data: {
           labels: labels,
           datasets: [
              {
                 data: data,
                 label: "Number of people",
                 fill: false,
                 lineTension: 0,
                 borderColor: "#08B46B",
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
        let temp_data = [];
        let temp_labels = [];
        let increment = 1;
        if(props.records.length > props.numPoints){
            increment = parseInt(props.records.length/props.numPoints);
        }
        
        for(let i = 0; i < props.records.length; i += increment){
            temp_data.push(props.records[i].count);
            temp_labels.push(props.records[i].time);
        }
        setData(temp_data);
        setLabels(temp_labels);
    },[ props.records, props.numPoints]);

    // React.useEffect(() => {
    //     const size = 60*60;
    //     let start = 30;

    //     let temp_data = [];
    //     let temp_labels = [];
    //     let increment = 1;
    //     if(size > props.numPoints){
    //         increment = parseInt(size/props.numPoints);
    //     }

    //     for(let i = 0; i < size; i += increment){
    //         start = Math.floor(Math.random()*3) + start - 1;
    //         temp_data.push(start);
    //         temp_labels.push("timetimetime"+ i);
    //     }
    //     setData(temp_data);
    //     setLabels(temp_labels);
    // },[ props.records, props.numPoints]);

    return(
        <Line
            data={chartData.data}
            options={chartData.options}
            height={600}
        />
    );
}

export default Statistics;
