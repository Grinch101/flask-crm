update contacts
    set comment = %s,
	posting_date = %s
WHERE row_id = %s
    AND contact_name = %s;