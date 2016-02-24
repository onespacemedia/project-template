export default {
  'root': {
    'appSrc': './{{cookiecutter.package_name}}/apps/**/assets',
    'src': './{{cookiecutter.package_name}}/assets',
    'dest': './{{cookiecutter.package_name}}/static/build'
  },

  'tasks': {
    'browserSync': {
      'notify': false,
      'open': false,
      'proxy': {
        'target': '0.0.0.0:8000'
      },
      'watch': [
        '{{cookiecutter.package_name}}/apps/**/templates/**/*.html',
        '{{cookiecutter.package_name}}/templates/**/*.html'
      ]
    },

    'js': {
      'src': 'js',
      'dest': 'js',
      'extractSharedJs': true,
      'entries': {
        'app': ['./main.js']
      },
      'extensions': ['js']
    },

    'css': {
      'src': 'css',
      'dest': 'css',
      'extensions': ['css']
    },

    'stylelint': {
      'src': 'css',
      'dest': 'css',
      'extensions': ['css']
    },

    'images': {
      'src': 'img',
      'dest': 'img',
      'extensions': ['jpg', 'png', 'svg', 'gif']
    },

    'fonts': {
      'src': 'fonts',
      'dest': 'fonts',
      'extensions': ['woff2', 'woff', 'eot', 'ttf', 'svg']
    }
  }
}