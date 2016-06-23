/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	'use strict';
	
	var app = angular.module('App', ['ngMaterial', 'md.data.table']); // jshint ignore:line
	
	// Syntax changed to prevent conflicts with jinja2
	app.config(['$interpolateProvider', function ($interpolateProvider) {
	    $interpolateProvider.startSymbol('{[');
	    $interpolateProvider.endSymbol(']}');
	}]);
	
	// The ng-model is does not support file inputs, so we create our own
	app.directive('fileModel', ['$parse', function ($parse) {
	    return {
	        restrict: 'A',
	        link: function link(scope, element, attrs) {
	            var model = $parse(attrs.fileModel);
	            var modelSetter = model.assign;
	
	            element.bind('change', function () {
	                scope.$apply(function () {
	                    modelSetter(scope, element[0].files[0]);
	                });
	            });
	        }
	    };
	}]);
	
	// Populate input fields if value is set
	app.directive('input', ['$parse', function ($parse) {
	    return {
	        restrict: 'E',
	        require: '?ngModel',
	        link: function link(scope, element, attrs) {
	            if (attrs.value && attrs.value !== 'None' && attrs.type !== "file") {
	                $parse(attrs.ngModel).assign(scope, attrs.value);
	            }
	        }
	    };
	}]);
	
	// List controller
	app.controller('AppCtrl', function ($scope, $log, $http, $filter, $mdSidenav, $mdDialog) {
	    // pathname without the inital forward slash
	    var pathname = window.location.pathname.substring(1);
	    var url_parts = ['/api', pathname];
	    var base_url = url_parts.join('/');
	
	    $scope.activeRecordIndex = false;
	    $scope.flashMessages = [];
	    $scope.formData = {};
	    $scope.imageFields = {};
	    $scope.isProcessing = false;
	    $scope.records = [];
	    $scope.selected = [];
	
	    $scope.populateForm = function (json_record) {
	        for (var key in json_record) {
	            if (key == 'start' || key == 'end') {
	                $scope.formData[key] = new Date(json_record[key]);
	            } else {
	                $scope.formData[key] = json_record[key];
	            }
	        }
	    };
	
	    // Set options for pagination
	    $scope.options = {
	        autoSelect: true,
	        boundaryLinks: false,
	        largeEditDialog: false,
	        pageSelector: false,
	        rowSelection: true
	    };
	
	    // Set query options for pagination
	    $scope.query = {
	        order: 'order',
	        limit: 50,
	        page: 1
	    };
	
	    // Simple replacement method of links
	    $scope.clearFlashMessage = function (index) {
	        $scope.flashMessages.splice(index, 1);
	    };
	
	    $scope.openNav = function () {
	        $mdSidenav('left').toggle();
	    };
	
	    $scope.deleteSelected = function () {
	        $scope.flashMessages = [];
	
	        // Appending dialog to document.body to cover sidenav in docs app
	        var confirm = $mdDialog.confirm().title('Delete item').content('Are you sure you want to remove the selected item(s)?').ariaLabel('Delete item').ok('Delete').cancel('Cancel').clickOutsideToClose(true);
	
	        $mdDialog.show(confirm).then(function () {
	            angular.forEach($scope.selected, function (item) {
	                // jshint ignore:line
	                var deleteUrl = [base_url, item.id].join('/');
	                // Remove item from backend
	                $http.delete(deleteUrl).success(function () {
	                    $scope.flashMessages.push(['Items deleted', 'success']);
	
	                    // Update the template with the records removed
	                    var selectedIndex = $scope.selected.indexOf(item);
	                    $scope.selected.splice(selectedIndex, 1);
	                    var recordsIndex = $scope.records.data.indexOf(item);
	                    $scope.records.data.splice(recordsIndex, 1);
	                    $scope.records.count = $scope.records.count - 1;
	                }).error(function (error) {
	                    $scope.flashMessages.push(['Failed to remove items, please try again.', 'warning']);
	                });
	            });
	        });
	    };
	
	    // Process a form
	    $scope.submitForm = function (_id) {
	        $scope.serverErrors = {};
	        $scope.flashMessages = [];
	        $scope.isProcessing = true;
	
	        var uploadUrl = base_url;
	        if (_id) {
	            uploadUrl = [base_url, _id].join('/');
	        }
	
	        // Create an empty FormData object to store all form fields
	        var fd = new FormData();
	
	        // Loop through all of the image fields, and append them to the FormData object
	        for (var key in $scope.imageFields) {
	            fd.append(key, $scope.imageFields[key], $scope.imageFields[key]['name']);
	        }
	
	        // Loop through all other fields, and append them to the FormData object
	        for (var key in $scope.formData) {
	            if ($scope.formData[key]) {
	                fd.append(key, $scope.formData[key]);
	            }
	        }
	
	        // Send the data of to the api, to be stored by the server
	        $http.post(uploadUrl, fd, {
	            transformRequest: angular.identity,
	            headers: { 'Content-Type': undefined }
	        }).success(function (result) {
	            window.location.href = $scope.cancel_url;
	        }).error(function (error, status) {
	            $scope.isProcessing = false;
	            var error_message = 'Something went wrong, please try again.';
	            if (error['message']) {
	                error_message = error['message'];
	            } else if (error['error']) {
	                error_message = error['error'];
	            }
	            $scope.flashMessages.push([error_message, 'warning']);
	            for (var key in error['data']) {
	                $scope.serverErrors[key] = error['data'][key];
	            }
	        });
	    };
	
	    $scope.reorder = function (event, record, increment) {
	        event.stopPropagation();
	        var fd = new FormData();
	        var firstIndex = $scope.records.data.indexOf(record);
	        var first_el = angular.copy($scope.records.data[firstIndex]);
	        var second_el = $scope.records.data.filter(function (obj) {
	            return obj['order'] == first_el['order'] + increment;
	        })[0];
	        var secondIndex = $scope.records.data.indexOf(second_el);
	
	        fd.append('ids', angular.toJson([{ 'id': first_el['id'], 'order': second_el['order'] }, { 'id': second_el['id'], 'order': first_el['order'] }]));
	
	        $http.put(base_url, fd, {
	            transformRequest: angular.identity,
	            headers: { 'Content-Type': undefined }
	        }).success(function (result) {
	            $scope.isProcessing = false;
	            $scope.records.data[firstIndex]['order'] = second_el['order'];
	            $scope.records.data[secondIndex]['order'] = first_el['order'];
	        }).error(function (error, status) {
	            $scope.isProcessing = false;
	            var error_message = 'Something went wrong, please try again.';
	            if (error['message']) {
	                error_message = error['message'];
	            } else if (error['error']) {
	                error_message = error['error'];
	            }
	            $scope.flashMessages.push([error_message, 'warning']);
	            for (var key in error['data']) {
	                $scope.serverErrors[key] = error['data'][key];
	            }
	        });
	    };
	});

/***/ }
/******/ ]);
//# sourceMappingURL=admin.js.map