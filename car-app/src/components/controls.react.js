import React from 'react';
import { Row, Col, Button, ButtonGroup, FormGroup } from 'reactstrap';

export default class MyControls extends React.Component {
  render() {
    return (
      <Row>
        <Col>
          <Row>
            <Col></Col>
            <Col className="d-flex justify-content-center">
              <Button>Forward</Button>
            </Col>
            <Col></Col>
          </Row>
          <Row>
            <Col className="d-flex justify-content-center">
              <Button>Left</Button>
            </Col>
            <Col className="d-flex justify-content-center">
              <Button>Stop</Button>
            </Col>
            <Col className="d-flex justify-content-center">
              <Button>Right</Button>
            </Col>
          </Row>
          <Row>
            <Col></Col>
            <Col className="d-flex justify-content-center">
              <Button>Back</Button>
            </Col>
            <Col></Col>
          </Row>
        </Col>
      </Row>
    );
  }
}
