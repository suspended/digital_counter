import React from 'react';
import {
    Container,
    Row,
    Col,
    Card
} from 'react-bootstrap';
import '../css/Homepage.css';

import {
    get_latest_count
} from '../services/API';

function Homepage() {
    let [ locations, setLocations] = React.useState([]);

    React.useEffect(() => {
        async function fetchCounter(){
            let response = await get_latest_count();
            setLocations(response.data);
        }
        fetchCounter();
        let  pollingInterval = setInterval(fetchCounter, 1000);
        return function cleanup(){
            clearInterval(pollingInterval);
        }
    },[]);

    const getColorForCount = (count, ok_limit, warning_limit) => {
        if(count > warning_limit){
            return "red" 
        } else if(count > ok_limit){
            return "yellow"
        }
        return "green";
    };


    return(
        <div className="counter_page d-flex align-items-center justify-content-center">
            <Container>
            {
                locations.map((location) => {
                    return (
                <Row key={location.id} className="counter_header p-3">
                    <Col md={"auto"}>
                        <Card>
                            <h1 className="display-1 text-center mx-3 px-3" id="counter" style={{color: getColorForCount(location.count,location.ok_limit,location.warning_limit)}}>{location.count}</h1>
                        </Card>
                    </Col>
                    <Col md="auto">
                        <h1>People in {location.name}</h1>
                        <p className="text-left" style={{color: "white"}}>
                            Updated on: {location.last_updated}
                        </p>
                    </Col>
                </Row>
                    )
                })
            }
            </Container>
        </div>
    );
}

export default Homepage;
