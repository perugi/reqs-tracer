from docx import Document
import re

req_id_pattern = r"SYSREQ-\d+"

reqs_doc = Document("requirements.docx")
arc_doc = Document("architecture.docx")

source_reqs = []

for paragraph in reqs_doc.paragraphs:
    match = re.search(req_id_pattern, paragraph.text)
    if match:
        source_reqs.append(match.group())


def get_heading_number(paragraph):
    heading_regex = r"^((\d+\.)+) [\w ]+"
    match = re.search(heading_regex, paragraph.text)
    if match:
        return match.group(0).strip()
    return None


arc_reqs = dict()
current_heading = ""

for paragraph in arc_doc.paragraphs:
    heading_number = get_heading_number(paragraph)
    if heading_number:
        current_heading = heading_number

    match = re.search(req_id_pattern, paragraph.text)
    if match:
        if arc_reqs[match.group()]:
            arc_reqs[match.group()].append(current_heading)
        else:
            arc_reqs[match.group()] = [current_heading]


trace_table = dict()
for source_req in source_reqs:
    trace_table[source_req] = arc_reqs.setdefault(
        source_req, ["Requirement not covered"]
    )

print(trace_table)
