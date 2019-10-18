import React from 'react';
import { Card, CardImg, CardText, CardBody, CardTitle, CardSubtitle, Button } from 'reactstrap';

export default class MyCard extends React.Component {
  render() {
    return (
      <Card body inverse>
        <CardImg top width="100%" src={this.props.url} alt="Card image cap"/>
      </Card>
    );
  }
}
