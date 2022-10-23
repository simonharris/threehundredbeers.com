DELETE FROM 3cbpostmeta;
DELETE FROM 3cbposts WHERE ID > 270 AND post_mime_type NOT IN ('image/jpeg');
DELETE FROM 3cbterm_relationships;