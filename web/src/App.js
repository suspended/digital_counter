import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import './css/App.css';

import Header from './components/common/Header';

import Homepage from './components/Homepage';
import Statistics from './components/Statistics';

function App() {
  return (
    <div>
      <Router>
        <Header />
        <Switch>
          <Route exact path='/' component={Homepage} />
          <Route exact path='/stats' component={Statistics} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
