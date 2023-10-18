const path = require('path');

module.exports = {
    mode: 'production',
    entry: './App.js',
    output: {
        path: path.resolve(__dirname, '../static/script'),
        filename: 'react_output.js',
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'] 
            }
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx']
    }
};
