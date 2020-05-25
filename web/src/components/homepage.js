import React from 'react';
import {
    Container,
    Row,
    Col,
    Card
} from 'react-bootstrap';

import '../css/Homepage.css';

function Homepage() {
    let [ count, setCount ] = React.useState(0);


    const getColorForCount = () => {
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
            </Container>
        </div>
    );
}

export default Homepage;
