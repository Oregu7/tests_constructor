TestMVC.module('TestsApp.List', function(List, TestMVC, Backbone, Marionette, $, _){
    List.Controller = {
        listTests: function(){
            var tests = TestMVC.request('tests:all');

            var testsListView = new List.TestsView({
                collection: tests
            });

            TestMVC.mainRegion.show(testsListView)
        }
    }
})
