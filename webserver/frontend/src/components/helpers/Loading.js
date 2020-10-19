import React, { Component } from 'react';


class Loading extends Component {
  render() {
    return(
      <div className="loading-container">
        <img className="center-loading-gif" src="/images/loading.gif" alt="Loading..." />
        <div className="loading-message-centered">Loading...</div>
      </div>
    )
  }
}

export default Loading;
