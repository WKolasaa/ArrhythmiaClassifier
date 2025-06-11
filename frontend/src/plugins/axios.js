import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://20.82.105.66:5001/',
});

export default instance;
