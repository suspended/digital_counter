import React from 'react';
import {
    Container,
    Row,
    Col,
    Form,
    Button
} from 'react-bootstrap';

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

    let [ startDate, setStartDate ] = React.useState("");
    let [ endDate, setEndDate ] = React.useState("");
    let [ locationID, setLocationID] = React.useState("");

    let [ recordList , setRecordList ] = React.useState([]);
    let [ max , setMax ] = React.useState(0);
    let [ min , setMin ] = React.useState(0);
    let [ avg , setAvg ] = React.useState(0);

    React.useEffect(() => {
        async function fetchData(){
            let location_response = await get_location();
            setLocationList(location_response.data);
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
        let statistic_response = await get_statistics(locationID, startDate, endDate);
        setRecordList(statistic_response.data.stats);
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
        setAvg(total/recordList.length);
    }, [recordList]);

    React.useEffect(() => {
        console.log(startDate);
        console.log(endDate);
    }, [startDate, endDate]);

    return(
        <Container>
            <Row>
                <Col sm="12" lg="3">
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
                <Col sm="12" lg="3" className="d-flex align-items-end flex-column">
                    <Button className="mt-auto mb-3" onClick={() =>{onClickStatistics()}}>Get Statistics</Button>
                </Col>
            </Row>
            <hr />
            <Row>
                
            </Row>
            <hr />
            <Row>
                <Col sm="12" lg="4">
                    <h3>Max: {max}</h3>
                </Col>
                <Col sm="12" lg="4">
                    <h3>Min: {min}</h3>
                </Col>
                <Col sm="12" lg="4">
                    <h3>Avg: {avg}</h3>
                </Col>
            </Row>
        </Container>
    );
}

export default Statistics;
