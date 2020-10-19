import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import LoginPageTemplate from './LoginPageTemplate';
import Loading from '../helpers/Loading';
import config from '../../configuration/config';
//import '../../css/App.css';

const apiUrl = (config.productionEnv) ? '' : 'http://' + config.backend.ip + ':' + config.backend.port;
const headers = config.backend.headers

class LoginPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
        username: '',
        password: '',
        submitted: false,
        loading: false,
        error: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleClose = this.handleClose.bind(this);

    // Set the state "loggedIn" in App.js
    this.props.parentCallback(!!Cookies.get('token'));
  }

  handleClose(event, reason) {
    if (reason === 'clickaway') {
      return;
    }

    this.setState({ error: '' });
  }

  handleChange(e) {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  }

  handleLogin(e) {
    e.preventDefault();

    this.setState({ submitted: true });
    const { username, password } = this.state;

    // stop here if form is invalid
    if (!(username && password)) {
        return;
    }

    this.setState({ loading: true });

    axios.post(`${apiUrl}${config.backend.urlPrefix}${config.backend.loginEndpoint}`,
      {
        username: username,
        password: password
      }, {
        headers: headers
      })
      .then((response) => {
        // useless timeout to virtualize the login request delays and see the awesome loading gif.
        setTimeout(
          function() {
            if (response.data.access_token !== undefined && response.data.status === 200) {
              Cookies.set('token', response.data.access_token)
              Cookies.set('refresh_token', response.data.refresh_token)

              // Set the state "loggedIn" in App.js
              this.props.parentCallback(!!response.data.access_token);

              this.props.history.push('/dashboard');
            } else {
              Cookies.remove('token')
              Cookies.remove('refresh_token')
              this.setState({ error: "Wrong Credentials.", loading: false })
            }
          }
          .bind(this),
          config.frontend.loadingPageDuration
        );
      }).catch(error => {
          console.log(error);
          Cookies.remove('token')
          Cookies.remove('refresh_token')
          this.setState({ error: error, loading: false })
      });
  }

  render() {
    return (
      this.state.loading
        ? <Loading />
        : <LoginPageTemplate state={this.state} handleLogin={this.handleLogin} handleChange={this.handleChange} handleClose={this.handleClose} />
    );
  }
}

export default LoginPage;
