import axios from "axios";

const API_SERVER = (process.env.REACT_APP_API_SERVER !== undefined) ? (process.env.REACT_APP_API_SERVER) : ("http://localhost:5000");
// const API_SERVER = (process.env.REACT_APP_API_SERVER !== undefined) ? (process.env.REACT_APP_API_SERVER) : ("https://dc-api.ernestlwt.com");

export function get_latest_count(){
    return axios.get(API_SERVER+'/location/get_latest_count');
}

export function get_location(){
    return axios.get(API_SERVER+'/location');
}

export function get_statistics(location_id, start_time, end_time){
    let data = new FormData();
    data.append('location_id', location_id);
    data.append('start_time', start_time);
    data.append('end_time', end_time);
    return axios.post(API_SERVER+'/location/statistics' ,data);
}

export function get_daily_statistics(location_id, target_date){
    let data = new FormData();
    data.append('location_id', location_id);
    data.append('target_date', target_date);
    return axios.post(API_SERVER+'/location/daily_statistics' ,data);
}