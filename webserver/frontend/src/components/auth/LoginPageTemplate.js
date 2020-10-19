import React, { Component } from 'react';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import config from '../../configuration/config';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

class LoginPageTemplate extends Component {
  render() {
    const { username, password, submitted, loading, error } = this.props.state;

    return(
      <div>
        <div className="tabs">
          {error &&
            <Snackbar open={!!error} autoHideDuration={config.frontend.alertAutoHideDuration} onClose={this.props.handleClose}>
              <Alert onClose={this.props.handleClose} severity="error">
                {error}
              </Alert>
            </Snackbar>}
          <div>
            <div id="logo">
              <h1 id="login"><i>  KSTS INDUSTRIES</i></h1>
            </div>
            <section className="jvs-login">
              <form action="" method="">
                <div id="fade-box">

                  <input type="text" name="username" id="username" placeholder="Username" value={username} onChange={this.props.handleChange} required/>
                  {submitted && !username &&
                    <div className="jvs-font-color">Username is required</div>
                  }

                  <input type="password" name="password" placeholder="Password" value={password} onChange={this.props.handleChange} required/>
                  {submitted && !password &&
                    <div className="jvs-font-color">Password is required</div>
                  }

                  <button disabled={loading} onClick={this.props.handleLogin}>Log In</button>
                </div>
              </form>
              <div className="hexagons">
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <br/>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <br/>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <br/>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <br/>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
                <span>&#x2B22;</span>
              </div>
            </section>

            <div id="circle1">
              <div id="inner-cirlce1">
                <h2> </h2>
              </div>
            </div>

            <ul>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
        </div>
      </div>
    )
  }
}

export default LoginPageTemplate;
