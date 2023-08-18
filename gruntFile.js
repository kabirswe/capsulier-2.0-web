module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		clean: {
			dist: {
				src: [
					'src/main/static/main/dist',
					'src/static/vendor',
				]
			},
			prefixed: {
				src: [
					'src/main/static/main/dist/prefixed',
				]
			}
		},

		sass: {
			dist: {
				files: {
					'src/main/static/main/css/capsulier.css' : 'src/main/static/main/scss/capsulier.scss',
					'src/main/static/main/css/conservatoire.css' : 'src/main/static/main/scss/conservatoire.scss',
				}
			}
		},

		watch: {
			sass: {
				files: 'src/**/*.scss',
				tasks: ['sass'],
			},
			css: {
				files: 'src/**/*.css',
				options: {
					livereload: true,
				},
			},
			html: {
				files: 'src/**/*.html',
				options: {
					livereload: true,
				},
			},
			js: {
				files: 'src/**/*.js',
				options: {
					livereload: true,
				},
			}
		},

		postcss: {
			options: {
				// map: true,
				processors: [
					require('autoprefixer')({browsers: ['last 100 version']})
				]
			},
			main: {
				files: [{
					expand: true,
					cwd: 'src/main/static/main/css/',
					src: ['*.css'],
					dest: 'src/main/static/main/dist/prefixed/',
					ext: '.css'
				}]
			},
		},

		cssmin: {
			main: {
				files: [{
					expand: true,
					cwd: 'src/main/static/main/dist/prefixed/',
					src: ['*.css'],
					dest: 'src/main/static/main/dist/',
					ext: '.min.css'
				}]
			},
			options: {
				mergeIntoShorthands: false,
				roundingPrecision: -1
			},
		},

		uglify: {
			options: {
				manage: false,
			},
			contact: {
				files: [{
					expand: true,
					cwd: 'src/contact/static/contact/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/contact/static/contact/dist/',
					ext: '.min.js'
				}]
			},
			main: {
				files: [{
					expand: true,
					cwd: 'src/main/static/main/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/main/static/main/dist/',
					ext: '.min.js'
				}]
			},
			account: {
				files: [{
					expand: true,
					cwd: 'src/static/account/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/static/account/dist/',
					ext: '.min.js'
				}]
			},
			blog: {
				files: [{
					expand: true,
					cwd: 'src/blog/static/blog/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/blog/static/blog/dist/',
					ext: '.min.js'
				}]
			},
			eshop: {
				files: [{
					expand: true,
					cwd: 'src/eshop/static/eshop/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/eshop/static/eshop/dist/',
					ext: '.min.js'
				}]
			},
			mycaps: {
				files: [{
					expand: true,
					cwd: 'src/mycaps/static/mycaps/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/mycaps/static/mycaps/dist/',
					ext: '.min.js'
				}]
			},
			page: {
				files: [{
					expand: true,
					cwd: 'src/page/static/page/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/page/static/page/dist/',
					ext: '.min.js'
				}]
			},
			infinite_scroll: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/infinite-scroll/',
						src: ['dist/**'],
						dest: 'src/static/vendor/infinite-scroll/',
					}
				]
			},
			product: {
				files: [{
					expand: true,
					cwd: 'src/product/static/product/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/product/static/product/dist/',
					ext: '.min.js'
				}]
			},
			userprofile: {
				files: [{
					expand: true,
					cwd: 'src/userprofile/static/userprofile/js/',
					src: ['*.js', '!*.min.js'],
					dest: 'src/userprofile/static/userprofile/dist/',
					ext: '.min.js'
				}]
			},
		},

		copy: {

			/*Main*/
			jquery: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/jquery/',
						src: ['dist/**'],
						dest: 'src/static/vendor/jquery/',
					}
				]
			},
			bootstrap: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/bootstrap/',
						src: ['dist/**'],
						dest: 'src/static/vendor/bootstrap/',
					}
				]
			},
			bootbox_js: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/',
						src: ['bootbox.js/**'],
						dest: 'src/static/vendor/',
					}
				]
			},
			bootstrap_datepicker: {
				files: [
				{
					expand: true,
					cwd: 'src/static/bower_components/bootstrap-datepicker/',
					src: ['dist/**'],
					dest: 'src/static/vendor/bootstrap-datepicker/',
				}
				]
			},
			font_awesome: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/font-awesome/',
						src: ['web-fonts-with-css/**'],
						dest: 'src/static/vendor/font-awesome/',
					}
				]
			},
			jquery_easing: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/jquery.easing/',
						src: ['js/**'],
						dest: 'src/static/vendor/jquery.easing/',
					}
				]
			},
			popper_js: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/popper.js/',
						src: ['dist/**'],
						dest: 'src/static/vendor/popper.js/',
					}
				]
			},
			slick_carousel: {
				files: [
					{
						expand: true,
						cwd: 'src/static/bower_components/slick-carousel/',
						src: ['slick/**'],
						dest: 'src/static/vendor/slick-carousel/',
					}
				]
			},
		},
	});

	grunt.loadNpmTasks('grunt-postcss');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-copy');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-uncss');
	grunt.loadNpmTasks('grunt-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.registerTask('default', [
		'clean:dist',
		'sass',
		'postcss',
		'cssmin',
		'clean:prefixed',
		'uglify',
		'copy',
	]);
};
