

import axios from 'axios'

const baseUrl = 'http://localhost:3001'

const createWallet = () => {
    return axios.post(baseUrl + '/wallet/create')
}

const getWallet = (public_key) => {
    return axios.post(baseUrl + '/wallet/info', {public_key})
}

const sendMoney = (attr) => {
    return axios.post(baseUrl + '/wallet/send', attr)
}

const mine = (public_key) => {
    return axios.post(baseUrl + '/mine', {reward_address: public_key})
}

export default {createWallet, getWallet, sendMoney, mine}