#Missy Dupreast - ACT 400

-- Change the delimiter to //
DELIMITER //
CREATE TRIGGER track_evidence_changes
AFTER INSERT ON evidence
FOR EACH ROW
BEGIN
INSERT INTO evidence_changes (evidence_id, action, change_date)
VALUES (NEW.evidence_id, 'INSERT', NOW());
END;
//
-- Reset the delimiter
DELIMITER ;

# Test the trigger:
INSERT INTO evidence VALUES
(12, 'Document B');

INSERT INTO evidence VALUES
(13, 'Voicemail G');

SELECT * FROM evidence_changes;