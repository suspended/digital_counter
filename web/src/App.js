import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import './css/App.css';

import Homepage from './components/homepage';

function App() {
  return (
    <div>
      <Router>
        <Switch>
          <Route exact path='/' component={Homepage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
