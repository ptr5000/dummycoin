import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Client from './client.js'

class RegistrationForm extends Component {
  constructor(props) {
    super(props)
    this.state = {
      walletName: ''
    }
  }

  handleWalletNameChange = (event) => {
    this.setState({walletName: event.target.value})
  }

  handleLogin = (event) => {
    event.preventDefault();
    this
      .props
      .handleLogin(this.state.walletName)
  }

  render() {
    return (
      <div className="registrationForm">
        <form onSubmit={this.handleLogin}>
          <input value={this.state.walletName} onChange={this.handleWalletNameChange}/>
          <button type="submit">Log in</button>
        </form>
      </div>
    )
  }
}

class WalletInfo extends Component {
  constructor(props) {
    super(props)
    this.state = {
      walletData: ''
    }
  }

  updateWallet = () => {
    Client
      .getWallet(this.props.userdata.public_key)
      .then(response => {
        this.setState({walletData: response.data})
      })
  }

  componentDidMount() {
    this.interval = setInterval(this.updateWallet, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    return (
      <div className="walletInfo">
        <p>Balance: {this.state.walletData.balance}
          DC</p>
      </div>
    )
  }
}

class TransferForm extends Component {
  constructor(props) {
    super(props)
    this.state = {
      amount: '',
      toAddr: ''
    }
  }

  handleAmountChange = (event) => {
    this.setState({amount: event.target.value})
  }

  handleToAddrChange = (event) => {
    this.setState({toAddr: event.target.value})
  }

  handleTransfer = (event) => {
    event.preventDefault();
    
    let attrs = {amount: Number(this.state.amount), recipient: this.state.toAddr,  ...this.props.userdata}

    Client.sendMoney(attrs).then(response => {
      console.log(response)
    })
  }

  render() {
    return (
      <div className="transferForm">
        <form onSubmit={this.handleTransfer}>
          <label>Amount</label>
          <input value={this.state.amount} onChange={this.handleAmountChange}/>
          <label>To address</label>
          <input value={this.state.toAddr} onChange={this.handleToAddrChange}/>
         
          <button type="submit">Send money</button>
        </form>
      </div>
    )
  }
}
class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      userdata: null,
      username: null
    }
  }

  mine = () => {
    Client.mine(this.state.userdata.public_key)
  }

  handleLogin = (username) => {
    let userdata = localStorage.getItem(username)
    console.log(userdata);

    if (userdata === null) {
      Client
        .createWallet()
        .then(response => {
          console.log(response);
          this.setState({userdata: response.data, username: username})
          localStorage.setItem(username, JSON.stringify(response.data));
        })
    } else {
      this.setState({
        userdata: JSON.parse(userdata),
        username: username
      })
    }
  }

  render() {
    if (this.state.userdata == null) {
      return (
        <div className="App">

          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo"/>
            <h1 className="App-title">Welcome to DummyCoin</h1>
          </header>
          <p className="App-intro">
            To get started, log in to your wallet.
          </p>

          <RegistrationForm handleLogin={this.handleLogin}/>
        </div>
      );
    } else {
      return (
        <div>
          <h1 className="username">{this.state.username}</h1>
          <button className="minebutton" onClick={this.mine}>Mine</button>
          <div className="clearfix"></div>
          <WalletInfo userdata={this.state.userdata} />
          <TransferForm userdata={this.state.userdata} />
          
          <div className="keys">
            <p className="keyhead">Public key</p>
            <p className="publickey">{this.state.userdata.public_key}</p>
            <p className="keyhead">Private key</p>
            <p className="privatekey">{this.state.userdata.private_key}</p>
          </div>
        </div>
      );
    }
  }
}

export default App;
