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

import Statistics from './Statistics';

function Homepage() {
    let [ locations, setLocations] = React.useState([]);

    React.useEffect(() => {
        let polling = false;
        async function fetchCounter(){
            if(polling){
                return;
            }
            polling = true;
            let response = await get_latest_count();
            setLocations(response.data);
            polling = false;
        }
        fetchCounter();
        let  pollingInterval = setInterval(fetchCounter, 1000);
        return function cleanup(){
            clearInterval(pollingInterval);
        }
    },[]);

    const getColorForCount = (count, ok_limit, warning_limit) => {
        if(count > warning_limit){
            return "red"; 
        } else if(count > ok_limit){
            return "orange";
        }
        return "green";
    };

    const getTextForCount = (count, ok_limit, warning_limit) => {
        if(count > warning_limit){
            return "Crowded";
        } else if(count > ok_limit){
            return "Some Crowd";
        }
        return "Not Crowded";
    };


    return(
        <div>
            <Container fluid className="content_page py-5">
            {
                locations.map((location) => {
                    return (
                <Row key={location.id}>
                    <Col md={"auto"}>
                        <Card  style={{backgroundColor: getColorForCount(location.count,location.ok_limit,location.warning_limit)}}>
                            <h1 className="text-center mx-3 px-3" id="counter">
                                {getTextForCount(location.count,location.ok_limit,location.warning_limit)}
                            </h1>
                        </Card>
                    </Col>
                    <Col md="auto">
                        <h1 className="text-center">{location.name}</h1>
                        <p className="text-center" style={{color: "white"}}>
                            Updated on: {(new Date(location.last_updated)).toLocaleString()}
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
