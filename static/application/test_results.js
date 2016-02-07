var Result = Backbone.Model.extend({});
var Results = Backbone.PageableCollection.extend({
	model: Result,
	url: window.location.href,
	state: {
		pageSize: 10
	},
	mode: "client"
});
var test_results = new Results();

var columns = [
	{
		name: "id",
		label: "ID",
		editable: false,
		cell: Backgrid.IntegerCell.extend({
      		orderSeparator: ''
    	})
	},

	{
		name: "name",
		label: "Фамилия",
		editable: false,
		cell: "string"
	},

	{
		name: "precent",
		label: "Процент",
		editable: false,
		cell: "number"
	},

	{
		name: "mark",
		label: "Оценка",
		editable: false,
		cell: "integer"
	},

	{
		name: "date",
		label: "Дата",
		editable: false,
		cell: "datetime"
	}
];

var grid = new Backgrid.Grid({
	columns: columns,
	collection: test_results
});

$('#results').append(grid.render().el);

var paginator = new Backgrid.Extension.Paginator({
	collection: test_results
});

$('#results').after(paginator.render().el);

var filter = filter = new Backgrid.Extension.ClientSideFilter({
  collection: test_results,
  fields: ['name']
});

$('#results').before(filter.render().el);
$(filter.el).css({float: "right", margin: "20px"});

test_results.fetch({reset:true})