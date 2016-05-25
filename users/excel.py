class Format():
    title = {
        'bold': True,
        'font_size': 20,
        'align': 'left',
        'valign': 'vcenter'
    }

    sub_title = {
        'bold': False,
        'bg_color': '#F7F7F7',
        'font_size': 15,
        'align': 'left',
        'valign': 'vcenter'
    }

    thead = {
        'bold': False,
        'bg_color': '#F8F8FF',
        'font_size': 15,
        'align': 'center',
        'valign': 'top'
    }

    item = {
        'bold': False,
        'font_size': 14,
        'align': 'center',
        'valign': 'top'
    }

    formula_res = {
        'bold': True,
        'bg_color': '#F8F8FF',
        "color": "red",
        'font_size': 15,
        'align': 'right',
        'valign': 'top'
    }

    formula_res2 = {
        'bold': True,
        'bg_color': '#F8F8FF',
        "color": "red",
        'font_size': 15,
        'align': 'left',
        'valign': 'top'
    }

    def write_param(self, sheet, style, item_style, key, value, index):
        sheet.merge_range("B%d:C%d" % (index, index), key, style)
        sheet.merge_range("D%d:G%d" % (index, index), value, item_style)

    def write_thead(self, sheet, style, items, row, col):
        for item in items:
            sheet.write(row, col, item, style)
            col += 1