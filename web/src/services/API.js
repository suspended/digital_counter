import axios from "axios";

const API_SERVER = (process.env.REACT_APP_API_SERVER !== undefined) ? (process.env.REACT_APP_API_SERVER) : ("http://localhost:5000");

export function get_latest_count(){
    return axios.get(API_SERVER+'/location/get_latest_count');
}

export function get_location(){
    return axios.get(API_SERVER+'/location');
}