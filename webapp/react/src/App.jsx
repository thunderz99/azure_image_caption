import React from 'react';
import logo from './logo.svg';
import './App.css';
import Dropzone from 'react-dropzone'
import fetch from 'node-fetch'

class App extends React.Component {
  constructor() {
    super()
    this.state = { files: [] }
  }

  onDrop(files) {

    var formData = new FormData();
    for (const file of files) {
      formData.append('file[]', file);
    }

    fetch('/flask/uploader', {
      method: 'POST',
      body: formData
    }).then(res => {
      res.json().then(json => {
        console.log('res:' + json)
        this.setState({ files: json })
      })
    }).catch(e => {
      console.log('Error', e);
    });


    this.setState({
      files
    });
  }

  render() {

    const dropStyle = { width: '100%' }
    const imgWidth = '300px'

    return (
      <section>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">画像認識Demo - どんな画像なのかを説明してくれる</h1>
          </header>
        </div>
        <div style={{ height: '10px' }} />
        <div className="dropzone" style={dropStyle}>
          <Dropzone onDrop={this.onDrop.bind(this)}
            accept="image/*"
            style={{
              "width": "90%",
              "height": 150,
              "borderWidth": 2,
              "borderColor": "#666",
              "borderStyle": "dashed",
              "borderRadius": 5,
              "margin": "auto"
            }}
          >
            <p>画像を選択してください</p>
          </Dropzone>
        </div>
        <aside>
          <h3>結果</h3>
          <ul>
            {
              this.state.files.map(f => <li key={f.filename}><img width={imgWidth} src={f.url} /><h3>{f.result}</h3></li>)
            }
          </ul>
        </aside>
      </section>
    );
  }
}

<App />

export default App;
