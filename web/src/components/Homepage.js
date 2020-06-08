import React from 'react';
import {
    Container,
    Row,
    Col
} from 'react-bootstrap';
import '../css/Homepage.css';

import {
    get_latest_count
} from '../services/API';

import DailyStatistics from './DailyStatistics';

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
        <div className="">
            <Container className="content_page pt-3">
                <Row className="border-bottom border-success p-3 text-center">
                    <Col></Col>
                    {
                        locations.map((location) => {
                            return (
                    <Col key={location.id} md={"auto"}>
                        <h3 className="text-center">{location.name}</h3>
                        <h1 className="text-center m-3 p-3" id="counter" style={{backgroundColor: getColorForCount(location.count,location.ok_limit,location.warning_limit)}}>
                            {getTextForCount(location.count,location.ok_limit,location.warning_limit)}
                        </h1>
                        <p className="text-center">
                            Updated on: <strong>{(new Date(location.last_updated)).toLocaleString()}</strong>
                        </p>
                    </Col>
                            )
                        })
                    }
                    <Col></Col>
                </Row>
            </Container>
            <DailyStatistics />
        </div>
    );
}

export default Homepage;
