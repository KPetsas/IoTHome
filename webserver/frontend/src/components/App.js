import React, { Component } from "react";
import Cookies from 'js-cookie';
import LoginPage from "./auth/LoginPage";
import Dashboard from "./dashboard/Dashboard";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

const ProtectedRoute = ({ component: Comp, loggedIn, path, ...rest }) => {
  return (
    <Route
      path={path}
      {...rest}
      render={(props) => {
        return loggedIn ? (
          <Comp {...props} />
        ) : (
          <Redirect
            to={{
              pathname: "/",
              state: {
                prevLocation: path,
                error: "You need to login first!",
              },
            }}
          />
        );
      }}
    />
  );
};

class Main extends Component {
  constructor() {
    super();
    this.state = {
      loggedIn: false,
    };
  }

  callbackFunction = (isLoggedIn) => {this.setState({loggedIn: isLoggedIn})}

  render() {
    return(
      <BrowserRouter>
        <Switch>
          <Route exact path="/" render={props => <LoginPage parentCallback={this.callbackFunction} location={props.location} history={props.history} />} />
          <ProtectedRoute path="/dashboard" loggedIn={Cookies.get('token') || this.state.loggedIn} component={Dashboard} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default Main
