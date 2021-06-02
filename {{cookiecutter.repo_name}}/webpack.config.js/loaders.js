const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const JSLoader = {
  test: /\.js$/,
  exclude: /node_modules/,
  use: {
    loader: 'babel-loader',
    options: {
      presets: ['@babel/preset-env'],
      plugins: ['@babel/plugin-transform-object-assign']
    }
  }
};

const ESLintLoader = {
  test: /\.js$/,
  enforce: 'pre',
  exclude: /node_modules/,
  use: {
    loader: 'eslint-loader',
    options: {
      configFile: path.resolve(__dirname, '../.eslintrc.js')
    },
  }
};

const VueLoader = {
  test: /\.vue$/,
  exclude: /node_modules/,
  use: {
    loader: 'vue-loader',
  }
};

const CSSLoader = {
  test: /\.css$/,
  exclude: /node_modules/,
  use: [
    {
      loader: MiniCssExtractPlugin.loader,
      options: {
        publicPath: path.resolve(__dirname, '../{{cookiecutter.package_name}}/assets/css')
      }
    },
    {
      loader: 'css-loader',
      options: {
        importLoaders: 1,
        sourceMap: true,
      },
    },
    {
      loader: 'postcss-loader',
      options: {
        config: {
          path: path.resolve(__dirname, '../postcss.config.js')
        },
        sourceMap: true,
      },
    },
  ],
};

const FileLoader = {
  test: /\.(png|svg|jpg|jpeg|gif)$/,
  exclude: /node_modules/,
  use: {
    loader: 'file-loader',
    options: {
      name: 'img/[name].[ext]',
    },
  },
};

const FontLoader = {
  test: /\.(woff|woff2|eot|ttf|otf)$/,
  exclude: /node_modules/,
  use: {
    loader: 'file-loader',
    options: {
      name: 'fonts/[name].[ext]',
    },
  },
}

module.exports = {
  JSLoader,
  ESLintLoader,
  CSSLoader,
  VueLoader,
  FileLoader,
  FontLoader
};
