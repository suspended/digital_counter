import axios from "axios";

const API_SERVER = (process.env.REACT_APP_API_SERVER !== undefined) ? (process.env.REACT_APP_API_SERVER) : ("http://localhost:5000");

export function get_count(){
    return axios.get(API_SERVER+'/get_counter');
}

export function get_threshold(){
    return axios.get(API_SERVER+'/get_threshold');
}