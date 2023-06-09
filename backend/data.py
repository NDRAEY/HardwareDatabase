def prepare_table_fields(db):
    "Prepare needed table fields (just remove the `_id` field)"

    fields = list(db.table_fields.find({}))[0]

    del fields['_id']

    return fields