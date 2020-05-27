import React from 'react';
import {
    Container,
    Row,
    Col,
    Card
} from 'react-bootstrap';
import '../css/Homepage.css';

import {
    get_count,
    get_threshold
} from '../services/API';

function Homepage() {
    let [ count, setCount ] = React.useState(0);
    let [ lastUpdated, setLastUpdated ] =  React.useState("");
    let [ okLimit, setOkLimit ] = React.useState(50);
    let [ warningLimit, setWarningLimit ] = React.useState(50);

    React.useEffect(() => {
        async function fetchCounter(){
            let response_count = await get_count();
            setCount(response_count.data.count);
            let updateDate = new Date(response_count.data.last_updated);
            setLastUpdated(updateDate.toLocaleString());
        }
        async function fetchThreshold(){
            let response_threshold = await get_threshold();
            setOkLimit(response_threshold.data.ok_limit);
            setWarningLimit(response_threshold.data.warning_limit);
        }
        fetchCounter();
        fetchThreshold();
        let  pollingInterval = setInterval(fetchCounter, 3000);
        return function cleanup(){
            clearInterval(pollingInterval);
        }
    },[]);

    const getColorForCount = () => {
        if(count > warningLimit){
            return "red" 
        } else if(count > okLimit){
            return "yellow"
        }
        return "green";
    };


    return(
        <div className="counter_page d-flex align-items-center justify-content-center">
            <Container fluid>
                <Row className="counter_header">
                    <Col>
                        <h1 className="display-2">Current Count</h1>
                    </Col>
                </Row>
                <Row>
                    <Col></Col>
                    <Col md={"auto"}>
                        <Card>
                            <h1 className="display-1 text-center mx-3 px-3" id="counter" style={{color: getColorForCount(count)}}>{count}</h1>
                        </Card>
                    </Col>
                    <Col></Col>
                </Row>
                <Row className="pt-3">
                    <Col>
                        <p style={{color: "white"}}>
                        Updated on: {lastUpdated}
                        </p>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Homepage;
