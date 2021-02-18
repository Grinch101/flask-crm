update contacts
    set comment = %s,
	posting_date = %s
WHERE id = %s
    AND contact_name = %s;