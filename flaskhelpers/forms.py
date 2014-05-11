# Various helper functions related to forms

def extract_post_data(request, required_fields):
    '''
    Returns (data,errors) tuple. errors is false upon success

    Example usage:

    >>> @app.route('/process', methods=['POST'])
    >>> def process():
        >>> required_fields = ('username', 'password')
        >>> data,errors = extract_post_data(request, required_fields)
        ...
        >>> return render_template("home.html", data=data)
    '''
    errors = {}
    data = False
    form = request.form
    provided_fields = form.keys()
    missing_fields = [x for x in required_fields if x not in provided_fields]

    if missing_fields:
        errors['missing'] = missing_fields
        return (data, errors)

    data = dict([(k,form[k]) for k in provided_fields])
    return (data, errors)

