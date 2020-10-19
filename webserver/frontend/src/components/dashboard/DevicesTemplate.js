import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Switch from '@material-ui/core/Switch';
import { CircularProgress, Button } from '@material-ui/core';
import Title from './Title';

class DevicesTemplate extends Component {
  render() {
    return(
      <React.Fragment>
        <Title>Smart Devices</Title>

        <Table size="medium">
          <TableHead>
            <TableRow>
              <TableCell>Device</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>State</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {this.props.state.rows.map((row) => (
              <TableRow key={row.device_ui_id}>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.status}</TableCell>
                <TableCell>{row.state}</TableCell>
                <TableCell align="right">
                  { row.device_ui_id === "door_opener"
                    ? <Button variant="contained" onClick={this.props.handleClick.bind(this, "door_opener")} disabled={this.props.state.doorBtnLoading}>
                        {this.props.state.doorBtnLoading && <CircularProgress size={23} />}
                        {!this.props.state.doorBtnLoading && 'Open'}
                      </Button>
                    : <Switch color="primary" checked={row.switch_state} value={row.device_ui_id} onChange={this.props.handleSwitchChange} inputProps={{ 'aria-label': 'primary checkbox' }} />
                  }
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

      </React.Fragment>
    )
  }
}

export default DevicesTemplate;
