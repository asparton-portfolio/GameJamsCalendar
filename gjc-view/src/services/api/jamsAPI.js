import axios from 'axios';

const JAMS_URI = '/jams';

export async function getJams(count = 50, when = 'upcoming') {
    const response = await axios.get(
        process.env.REACT_APP_API_URL + JAMS_URI + `?count=${count}&when=${when}`
    );

    if (response.status !== 200)
        return new Error('Internal Server Error');
    else
        return response.data;
}

export async function insertJam(jam) {
    const response = await axios.post(
        process.env.REACT_APP_API_URL + JAMS_URI,
        jam
    );

    if (response.status !== 201)
        return new Error(response.data);
    else
        return response.data;
}