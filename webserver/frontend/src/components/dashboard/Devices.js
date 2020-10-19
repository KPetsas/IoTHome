import React, { Component } from 'react';
import axios from 'axios';
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import Cookies from 'js-cookie';
import DevicesTemplate from './DevicesTemplate';
import Loading from '../helpers/Loading';
import config from '../../configuration/config';


const apiUrl = (config.productionEnv) ? '' : 'http://' + config.backend.ip + ':' + config.backend.port;

function getRowId(array, id) {
  return array.findIndex((obj => obj.device_ui_id === id));
}

class Devices extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: false,
      doorBtnLoading: false,
      rows: []
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleSwitchChange = this.handleSwitchChange.bind(this);
  }

  componentDidMount() {
    this.setState({ loading: true });

    // Function that will be called to refresh authorization when access token has expired. Intercept the original request when it fails, refresh the authorization and continue with the original request.
    const refreshAuthLogic = failedRequest => axios.post(`${apiUrl}${config.backend.urlPrefix}${config.backend.tokenRefreshEndpoint}`, {},
      {
        headers: { 'Authorization': 'Bearer ' + Cookies.get('refresh_token') }
      })
      .then(tokenRefreshResponse => {
        Cookies.set('token', tokenRefreshResponse.data.access_token)
        failedRequest.response.config.headers['Authorization'] = 'Bearer ' + tokenRefreshResponse.data.access_token;
        return Promise.resolve();
      }).catch(error => {
        console.log("Refresh token failed. Error: " + error);
        Cookies.remove('token')
        Cookies.remove('refresh_token')

        this.props.history.push('/');
        return Promise.reject(error);
      });

    // Instantiate the interceptor (pass the axios instance and the refresh function).
    createAuthRefreshInterceptor(axios, refreshAuthLogic);

    axios.get(`${apiUrl}${config.backend.urlPrefix}${config.backend.devicesEndpoint}`,
      {
        headers: { 'Authorization': 'Bearer ' + Cookies.get('token') }
      })
      .then((response) => {

        console.log(response.data.devices);

        this.setState({ rows: response.data.devices });
        this.setState({ loading: false });
      }).catch(error => {
        console.log(error);
        this.setState({ loading: false });
      });
  }

  handleClick(id) {
    if (id === 'door_opener') {
      console.log('Door opener');

      axios.get(`${apiUrl}${config.backend.urlPrefix}${config.backend.doorOpenerEndpoint}`,
        {
          headers: { 'Authorization': 'Bearer ' + Cookies.get('token') }
        })
        .then((response) => {
          // console.log(response.data.status);
          console.log(response.data.message);
          this.setState({ doorBtnLoading: true });
          setTimeout(() => this.setState({ doorBtnLoading: false }), config.frontend.doorBtnLoadingDuration);
        });
    }
  }

  handleSwitchChange(event) {
    let rowsArray = this.state.rows;

    // This variable is related to the backend's device_ui_id.
    const id = event.target.value;

    let deviceObj = rowsArray[getRowId(rowsArray, id)];

    if (id === 'alarm_switch') {
      console.log('Alarm switch');
    } else if (id === 'smart_socket') {
      console.log('Smart socket switch');

      var action = (event.target.checked) ? 'on' : 'off';

      axios.put(`${apiUrl}${config.backend.urlPrefix}${config.backend.wifiSwitchesEndpoint}`,
        {
          device_ui_id: deviceObj.device_ui_id,
          action: action
        }, {
          headers: { 'Authorization': 'Bearer ' + Cookies.get('token') }
        })
        .then((response) => {
          let data = response.data;
          console.log(data);
          deviceObj.status = data.status;
          deviceObj.state = data.state;
          deviceObj.switch_state = data.switch_state;

          this.setState({ rows: rowsArray });
        }).catch(error => {
          console.log(error);
        });
    }
  }

  render() {
    return (
      this.state.loading
        ? <Loading />
        : <DevicesTemplate state={this.state} handleSwitchChange={this.handleSwitchChange} handleClick={this.handleClick} />
    )
  }

}

export default Devices;
