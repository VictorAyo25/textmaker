"""The diagrams INS224's answers ask for, actually drawn.

    python scripts/author/ins224_figures.py

A model answer that says "three rectangles, a diamond labelled Places between
them" is not an answer to a drawing question. This draws them: entity
relationship diagrams in the course text's Chen notation, data flow diagrams at
every level, and use case diagrams with their boundary, actors and include
arrows.

Writes data/ins224/figures.json, a map of key to a finished <figure> block.
scripts/build-doing.mjs expands a {{fig:key}} marker in any authored answer, and
scripts/build-ins-pq.mjs appends figures to the past question answers, which are
lifted and carry no markers.

Every figure is stroked in currentColor on the white ground the manual's own
diagrams use, sized to stay legible at 560px, and carries an aria-label, because
a diagram nobody can read is no better than the sentence it replaced.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

WEBAPP = Path(__file__).resolve().parent.parent.parent
OUT = WEBAPP / "data" / "ins224" / "figures.json"

# ----------------------------------------------------------------- primitives
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, anchor="middle", bold=False, size=None, italic=False):
    bits = [f'x="{x}" y="{y}" text-anchor="{anchor}"']
    if bold:
        bits.append('font-weight="bold"')
    if size:
        bits.append(f'font-size="{size}"')
    if italic:
        bits.append('font-style="italic"')
    return f'<text {" ".join(bits)}>{esc(s)}</text>'


def box(x, y, w, h, label, rounded=0, bold=True, size=None):
    """An entity, an external agent, or any labelled rectangle."""
    r = f' rx="{rounded}"' if rounded else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="1.4"{r}/>']
    lines = label.replace("|", chr(10)).split("\n")
    first = y + h / 2 + 4 - (len(lines) - 1) * 7
    for i, line in enumerate(lines):
        out.append(text(x + w / 2, first + i * 14, line, bold=bold and i == 0, size=size))
    return "".join(out)


def diamond(cx, cy, w, h, label):
    """A Chen relationship."""
    pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
    return (
        f'<polygon points="{pts}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
        + text(cx, cy + 4, label, size=11)
    )


def oval(cx, cy, rx, ry, label, underline=False):
    """A Chen attribute. Underlined means it is the identifier."""
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="currentColor"/>']
    out.append(text(cx, cy + 3.5, label, size=10, bold=underline))
    if underline:
        half = min(rx - 4, 3.3 * len(label) / 2)
        out.append(
            f'<line x1="{cx - half}" y1="{cy + 6}" x2="{cx + half}" y2="{cy + 6}" stroke="currentColor"/>'
        )
    return "".join(out)


def store(x, y, w, label):
    """A DFD data store: an open ended rectangle, two parallel lines."""
    h = 26
    return (
        f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="currentColor" stroke-width="1.4"/>'
        f'<line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" stroke="currentColor" stroke-width="1.4"/>'
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" stroke="currentColor" stroke-width="1.4"/>'
        + text(x + w / 2 + 6, y + h / 2 + 4, label, size=11)
    )


def line(x1, y1, x2, y2, dashed=False, arrow=True, back=False):
    d = ' stroke-dasharray="5 4"' if dashed else ""
    a = ' marker-end="url(#insarrow)"' if arrow else ""
    b = ' marker-start="url(#insarrow)"' if back else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="1.3"{d}{a}{b}/>'


def actor(cx, cy, label):
    """A use case actor: stick figure with its name under it."""
    return (
        f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="currentColor" stroke-width="1.3"/>'
        f'<line x1="{cx}" y1="{cy + 7}" x2="{cx}" y2="{cy + 24}" stroke="currentColor" stroke-width="1.3"/>'
        f'<line x1="{cx - 10}" y1="{cy + 14}" x2="{cx + 10}" y2="{cy + 14}" stroke="currentColor" stroke-width="1.3"/>'
        f'<line x1="{cx}" y1="{cy + 24}" x2="{cx - 9}" y2="{cy + 38}" stroke="currentColor" stroke-width="1.3"/>'
        f'<line x1="{cx}" y1="{cy + 24}" x2="{cx + 9}" y2="{cy + 38}" stroke="currentColor" stroke-width="1.3"/>'
        + text(cx, cy + 52, label, size=11, bold=True)
    )


def usecase(cx, cy, label, rx=76, ry=19):
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="currentColor" stroke-width="1.3"/>'
        + text(cx, cy + 4, label, size=11)
    )


def figure(key, w, h, body, caption, label):
    """One finished figure, ready to drop into an answer."""
    svg = (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" '
        f'font-size="12" role="img" aria-label="{esc(label)}">'
        '<defs><marker id="insarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 1 L 9 5 L 0 9 z" fill="currentColor"/></marker></defs>'
        + body
        + "</svg>"
    )
    ET.fromstring(svg)  # a malformed figure stops the build
    return key, f'<figure class="eerfig">{svg}<figcaption>{caption}</figcaption></figure>'


FIGURES = {}


def add(*args):
    key, html = figure(*args)
    FIGURES[key] = html


# =================================================================== the ERDs
def chen_chain(entities, rels, attrs, y=150):
    """Entities in a row, diamonds between them, attributes as ovals joined to them.

    An attribute oval that floats unattached is not Chen notation and an examiner
    would mark it wrong, so every oval is drawn with the line that connects it to
    the entity it describes, meeting the nearest point of that entity's edge.
    """
    body = []
    for x, w, name in entities:
        body.append(box(x, y, w, 40, name))
    for cx, label, left, right in rels:
        body.append(diamond(cx, y + 20, 92, 40, label))
        body.append(line(left[0], y + 20, cx - 46, y + 20, arrow=False))
        body.append(line(cx + 46, y + 20, right[0], y + 20, arrow=False))
        body.append(text(left[1], y + 12, left[2], bold=True, size=12))
        body.append(text(right[1], y + 12, right[2], bold=True, size=12))
    for cx, cy, label, ident, ent in attrs:
        ex, ew, _ = entities[ent]
        anchor = min(max(cx, ex + 12), ex + ew - 12)
        below = cy > y
        body.append(
            line(cx, cy + (-15 if below else 15), anchor, y + (40 if below else 0), arrow=False)
        )
        body.append(oval(cx, cy, 44, 15, label, underline=ident))
    return "".join(body)


add(
    "restaurant-erd",
    700,
    250,
    chen_chain(
        entities=[(20, 110, "CUSTOMER"), (295, 110, "ORDER"), (570, 110, "MENU ITEM")],
        rels=[
            (202, "Places", (130, 140, "1"), (295, 285, "M")),
            (477, "Contains", (405, 415, "M"), (570, 560, "N")),
        ],
        attrs=[
            (60, 60, "customer_id", True, 0),
            (170, 95, "name", False, 0),
            (335, 60, "order_id", True, 1),
            (445, 95, "order_date", False, 1),
            (610, 60, "item_code", True, 2),
            (655, 105, "price", False, 2),
        ],
        y=150,
    )
    + text(350, 232, "Chen notation, as the course text draws it. Identifiers are underlined.", size=11, italic=True),
    "The restaurant ERD. One CUSTOMER places many ORDERs, so 1:M. One ORDER contains many MENU ITEMs and one item appears on many orders, so M:N, which is resolved with an associative entity when the model becomes tables.",
    "Entity relationship diagram: Customer places Order one to many, Order contains Menu Item many to many, in Chen notation",
)

add(
    "carrental-erd",
    700,
    320,
    chen_chain(
        entities=[(20, 110, "CUSTOMER"), (290, 120, "RENTAL"), (570, 110, "VEHICLE")],
        rels=[
            (200, "Makes", (130, 140, "1"), (290, 280, "M")),
            (480, "For", (410, 420, "M"), (570, 560, "1")),
        ],
        attrs=[
            (60, 60, "customer_id", True, 0),
            (170, 98, "licence_no", False, 0),
            (350, 60, "rental_id", True, 1),
            (350, 240, "start_date", False, 1),
            (610, 60, "vehicle_id", True, 2),
            (655, 105, "daily_rate", False, 2),
        ],
        y=150,
    )
    + text(
        350,
        288,
        "RENTAL is the associative entity: it turns one M:N into two 1:M relationships.",
        size=11,
        italic=True,
    )
    + text(
        350,
        306,
        "Ordinality: a RENTAL must have both, so mandatory; a CUSTOMER or VEHICLE may have none, so optional.",
        size=10,
        italic=True,
    ),
    "The car rental ERD. Customer to Vehicle is many to many, so the associative entity RENTAL carries the dates and the cost and splits it into two one to many relationships.",
    "Entity relationship diagram with an associative entity Rental between Customer and Vehicle",
)

add(
    "warehouse-erd",
    700,
    430,
    "".join(
        [
            box(20, 40, 125, 40, "TRUCK DRIVER", size=11),
            box(300, 40, 120, 40, "TRUCK"),
            box(570, 40, 110, 40, "STOCK"),
            box(20, 175, 125, 40, "MANAGER"),
            box(300, 175, 120, 40, "LABOURER"),
            box(520, 320, 130, 40, "STOREKEEPER", size=11),
            box(40, 320, 145, 40, "STOCK REPORT", size=11),
            # row one: the driver submits the truck, the truck may carry stock
            diamond(222, 60, 92, 38, "Submits"),
            line(145, 60, 176, 60, arrow=False),
            line(268, 60, 300, 60, arrow=False),
            text(158, 52, "1", bold=True),
            text(290, 52, "M", bold=True),
            diamond(495, 60, 92, 38, "Carries"),
            line(420, 60, 449, 60, arrow=False),
            line(541, 60, 570, 60, arrow=False),
            text(432, 52, "1", bold=True),
            text(558, 52, "M", bold=True),
            # row two: the manager instructs the labourer, who unloads the truck
            diamond(222, 195, 96, 38, "Instructs"),
            line(145, 195, 174, 195, arrow=False),
            line(270, 195, 300, 195, arrow=False),
            text(158, 187, "1", bold=True),
            text(290, 187, "M", bold=True),
            diamond(360, 127, 92, 38, "Unloads"),
            line(360, 80, 360, 108, arrow=False),
            line(360, 146, 360, 175, arrow=False),
            text(372, 96, "M", bold=True),
            text(372, 168, "1", bold=True),
            # the storekeeper counts the stock and produces the report
            diamond(612, 195, 92, 38, "Counts"),
            line(625, 80, 612, 176, arrow=False),
            line(612, 214, 585, 320, arrow=False),
            text(634, 100, "M", bold=True),
            text(600, 300, "1", bold=True),
            diamond(352, 340, 100, 38, "Produces"),
            line(185, 340, 302, 340, arrow=False),
            line(402, 340, 520, 340, arrow=False),
            text(198, 332, "M", bold=True),
            text(508, 332, "1", bold=True),
            text(
                350,
                400,
                "A truck may or may not be carrying stock, so TRUCK to STOCK is optional at the stock end.",
                size=11,
                italic=True,
            ),
            text(
                350,
                417,
                "The report goes to the manager, the labourer and the driver: flows, not relationships, so they belong on the DFD.",
                size=10,
                italic=True,
            ),
        ]
    ),
    "The warehouse ERD. Every relationship is a named diamond with its cardinality: the driver submits trucks, a truck may carry stock, the manager instructs labourers, a labourer unloads trucks, and the storekeeper counts stock and produces the report.",
    "Entity relationship diagram for the warehouse receiving process with Truck Driver, Truck, Stock, Manager, Labourer, Storekeeper and Stock Report",
)

add(
    "sales-erd",
    700,
    250,
    chen_chain(
        entities=[(20, 130, "SALES REP"), (300, 120, "CUSTOMER"), (580, 100, "ORDER"), ],
        rels=[
            (215, "Serves", (150, 162, "1"), (300, 288, "M")),
            (490, "Places", (420, 432, "1"), (580, 570, "M")),
        ],
        attrs=[
            (70, 60, "rep_id", True, 0),
            (350, 60, "customer_id", True, 1),
            (630, 60, "order_id", True, 2),
        ],
        y=150,
    )
    + box(300, 40, 0, 0, "")
    + text(
        350,
        232,
        "Each order contains one or more PRODUCTs, and each product is stored in one WAREHOUSE: add both as a second row if the marks allow.",
        size=10,
        italic=True,
    ),
    "The sales management ERD. One sales representative serves many customers, each customer is served by one; one customer places many orders, each order belongs to one.",
    "Entity relationship diagram for a sales management system: Sales Rep serves Customer, Customer places Order",
)

add(
    "researchers-erd",
    640,
    240,
    chen_chain(
        entities=[(20, 130, "INSTITUTION"), (270, 130, "RESEARCHER"), (520, 100, "INTEREST")],
        rels=[
            (200, "Employs", (150, 160, "1"), (270, 260, "M")),
            (450, "Has", (400, 412, "M"), (520, 512, "N")),
        ],
        attrs=[(70, 60, "inst_id", True, 0), (330, 60, "staff_id", True, 1), (570, 60, "topic", True, 2)],
        y=150,
    )
    + text(
        320,
        222,
        "Each researcher is associated with one institution, so 1:M; each has several interests, so M:N.",
        size=11,
        italic=True,
    ),
    "The researchers ERD. One institution employs many researchers and each researcher belongs to one, which is 1:M. A researcher has several interests and an interest is shared by many researchers, which is M:N.",
    "Entity relationship diagram for researchers, institutions and research interests",
)

add(
    "pharmacy-erd",
    700,
    300,
    "".join(
        [
            box(20, 130, 110, 40, "PATIENT"),
            box(290, 130, 120, 40, "PRESCRIPTION"),
            box(570, 130, 110, 40, "DRUG"),
            box(290, 20, 120, 40, "DOCTOR"),
            diamond(205, 150, 92, 38, "Receives"),
            line(130, 150, 159, 150, arrow=False),
            line(251, 150, 290, 150, arrow=False),
            text(142, 142, "1", bold=True),
            text(280, 142, "M", bold=True),
            diamond(490, 150, 92, 38, "Appears on"),
            line(410, 150, 444, 150, arrow=False),
            line(536, 150, 570, 150, arrow=False),
            text(424, 142, "M", bold=True),
            text(558, 142, "1", bold=True),
            diamond(350, 95, 88, 36, "Writes"),
            line(350, 60, 350, 77, arrow=False),
            line(350, 113, 350, 130, arrow=False),
            text(362, 72, "1", bold=True),
            text(362, 126, "M", bold=True),
            line(65, 95, 75, 130, arrow=False),
            oval(65, 80, 44, 15, "patient_id", True),
            line(420, 225, 390, 170, arrow=False),
            oval(420, 240, 50, 15, "prescription_id", True),
            line(272, 225, 310, 170, arrow=False),
            oval(272, 240, 40, 15, "dose", False),
            line(625, 95, 625, 130, arrow=False),
            oval(625, 80, 40, 15, "drug_code", True),
            text(
                350,
                288,
                "PRESCRIPTION is the associative entity: it holds the date, the dose and who dispensed it.",
                size=10,
                italic=True,
            ),
        ]
    ),
    "The pharmacy ERD. Patient to Drug is many to many, so PRESCRIPTION resolves it and gives the date, dose and dispensing pharmacist somewhere to live. One doctor writes many prescriptions, each written by exactly one.",
    "Entity relationship diagram for a hospital pharmacy with Patient, Prescription, Drug and Doctor",
)

add(
    "ie-cardinality",
    660,
    260,
    "".join(
        [
            text(330, 24, "The same three cardinalities in Information Engineering, or crow's foot, style", bold=True, size=12),
            box(30, 50, 110, 34, "EMPLOYEE", size=11),
            box(420, 50, 110, 34, "LOGIN", size=11),
            line(140, 67, 420, 67, arrow=False),
            f'<line x1="150" y1="57" x2="150" y2="77" stroke="currentColor" stroke-width="1.4"/>',
            f'<line x1="410" y1="57" x2="410" y2="77" stroke="currentColor" stroke-width="1.4"/>',
            text(280, 58, "one to one", size=11, italic=True),
            box(30, 120, 110, 34, "CUSTOMER", size=11),
            box(420, 120, 110, 34, "ORDER", size=11),
            line(140, 137, 420, 137, arrow=False),
            f'<line x1="150" y1="127" x2="150" y2="147" stroke="currentColor" stroke-width="1.4"/>',
            f'<path d="M 420 137 L 405 127 M 420 137 L 405 137 M 420 137 L 405 147" stroke="currentColor" stroke-width="1.4" fill="none"/>',
            text(280, 128, "one to many", size=11, italic=True),
            box(30, 190, 110, 34, "STUDENT", size=11),
            box(420, 190, 110, 34, "COURSE", size=11),
            line(140, 207, 420, 207, arrow=False),
            f'<path d="M 140 207 L 155 197 M 140 207 L 155 207 M 140 207 L 155 217" stroke="currentColor" stroke-width="1.4" fill="none"/>',
            f'<path d="M 420 207 L 405 197 M 420 207 L 405 207 M 420 207 L 405 217" stroke="currentColor" stroke-width="1.4" fill="none"/>',
            text(280, 198, "many to many", size=11, italic=True),
            f'<circle cx="168" cy="207" r="5" fill="none" stroke="currentColor" stroke-width="1.4"/>',
            text(548, 240, "a circle is optional, a minimum of zero", size=10, anchor="end"),
            text(548, 100, "a bar is mandatory, a minimum of one", size=10, anchor="end"),
        ]
    ),
    "Cardinality in Information Engineering style: a bar across the line means one, a crow's foot means many, and a circle at the line's end means the participation is optional, a minimum of zero. Cardinality is the maximum, ordinality the minimum.",
    "Crow's foot notation showing one to one, one to many and many to many, with the bar for mandatory and the circle for optional",
)


# =================================================================== the DFDs
add(
    "landlord-context",
    660,
    280,
    "".join(
        [
            box(250, 110, 160, 60, "0\nLETTINGS SYSTEM", rounded=14),
            box(30, 40, 120, 40, "LANDLORD"),
            box(30, 200, 120, 40, "AGENT"),
            box(510, 120, 120, 40, "SUPERVISOR"),
            line(150, 60, 250, 118),
            text(196, 80, "house details", size=10),
            line(250, 160, 150, 206),
            text(186, 190, "agreement", size=10),
            line(150, 222, 250, 172),
            text(196, 240, "rent payment", size=10),
            line(410, 132, 510, 132),
            text(462, 122, "availability", size=10),
            line(510, 152, 410, 152),
            text(462, 168, "rent paid", size=10),
            text(
                330,
                262,
                "One process, numbered 0, the whole system. No data stores on a context diagram.",
                size=11,
                italic=True,
            ),
        ]
    ),
    "The context diagram. The whole lettings system is one process numbered 0, with the three external agents around it and only the flows that cross the boundary.",
    "Context diagram: one process, the lettings system, with Landlord, Agent and Supervisor as external agents",
)

add(
    "landlord-dfd1",
    680,
    300,
    "".join(
        [
            box(20, 130, 110, 40, "SUPERVISOR"),
            box(180, 40, 130, 52, "3.1\nRECEIVE RENT", rounded=12),
            box(180, 200, 130, 52, "3.2\nRECORD PAYMENT", rounded=12),
            box(400, 120, 130, 52, "3.3\nFORWARD TO\nLANDLORD", rounded=12, size=11),
            box(560, 130, 100, 40, "LANDLORD"),
            store(180, 130, 150, "D3 Payment"),
            line(130, 145, 180, 70),
            text(150, 96, "rent", size=10),
            line(310, 66, 400, 126),
            text(360, 88, "amount", size=10),
            line(245, 92, 245, 130, arrow=True),
            text(300, 118, "logged", size=10),
            line(245, 200, 245, 158, arrow=True),
            line(310, 226, 400, 172),
            text(360, 212, "receipt", size=10),
            line(530, 146, 560, 146),
            text(545, 128, "payment", size=10),
            text(
                340,
                285,
                "Level 1 explodes process 3.0 only. The rent that entered 3.0 enters 3.1, the payment that left it leaves 3.3: it balances.",
                size=10,
                italic=True,
            ),
        ]
    ),
    "The Level 1 DFD of rent payment, process 3.0 exploded into 3.1, 3.2 and 3.3. Its inputs and outputs are the same as the parent's, which is what balancing means.",
    "Level 1 data flow diagram exploding the rent payment process into receive rent, record payment and forward to landlord",
)

add(
    "clinic-context",
    660,
    270,
    "".join(
        [
            box(250, 105, 170, 60, "0\nCLINIC APPOINTMENT\nSYSTEM", rounded=14, size=11),
            box(30, 40, 110, 40, "PATIENT"),
            box(30, 190, 110, 40, "DOCTOR"),
            box(520, 40, 110, 40, "PHARMACY"),
            box(500, 190, 140, 40, "HEALTH COMMITTEE", size=10),
            line(140, 60, 250, 115),
            text(196, 78, "appointment request", size=9),
            line(250, 135, 140, 200),
            text(190, 182, "day's list", size=9),
            line(140, 210, 250, 155),
            text(196, 226, "consultation notes", size=9),
            line(420, 120, 520, 70),
            text(470, 96, "prescription", size=9),
            line(520, 80, 420, 135),
            text(470, 140, "dispensing record", size=9),
            line(420, 155, 500, 200),
            text(470, 188, "monthly report", size=9),
            text(330, 255, "The clerk, nurse and administrator are INSIDE the system: their work is the processes.", size=11, italic=True),
        ]
    ),
    "The clinic context diagram. Only the Patient, Doctor, Pharmacy and Health Committee sit outside the boundary; the clerk, nurse and administrator work inside the system, so their work becomes processes rather than agents.",
    "Context diagram for a campus clinic appointment system with four external agents",
)

add(
    "clinic-dfd0",
    720,
    440,
    "".join(
        [
            box(20, 30, 100, 36, "PATIENT"),
            box(600, 250, 100, 36, "PHARMACY"),
            box(590, 110, 110, 36, "COMMITTEE", size=11),
            box(600, 360, 100, 36, "DOCTOR"),
            box(250, 20, 140, 50, "1.0|BOOK APPOINTMENT", rounded=12, size=10),
            box(250, 110, 140, 50, "2.0|PREPARE CLINIC", rounded=12, size=10),
            box(250, 225, 140, 56, "3.0|RECORD|CONSULTATION", rounded=12, size=10),
            box(430, 245, 130, 50, "4.0|ISSUE|PRESCRIPTION", rounded=12, size=10),
            box(430, 110, 130, 46, "5.0|PRODUCE REPORT", rounded=12, size=10),
            store(30, 165, 150, "D3 Doctor Timetable"),
            store(30, 300, 140, "D1 Patient File"),
            store(30, 370, 140, "D2 Appointment"),
            line(120, 45, 250, 45),
            text(185, 36, "request", size=9),
            line(250, 58, 120, 58),
            text(185, 74, "slip", size=9),
            line(250, 55, 182, 170, arrow=False),
            line(182, 180, 250, 132),
            text(212, 152, "checks", size=9),
            line(252, 145, 172, 378),
            text(200, 250, "writes", size=9),
            line(320, 160, 320, 225),
            text(336, 196, "day's list", size=9),
            line(250, 258, 174, 306),
            text(196, 296, "notes", size=9),
            line(174, 322, 250, 278),
            text(214, 332, "reads", size=9),
            line(390, 268, 430, 268),
            text(410, 258, "drugs", size=9),
            line(560, 266, 600, 266),
            text(580, 256, "script", size=9),
            line(600, 280, 562, 286),
            text(584, 300, "dispensed", size=9),
            line(392, 240, 430, 152),
            text(438, 210, "attendances", size=9),
            line(560, 130, 590, 128),
            text(578, 112, "report", size=9),
            line(600, 366, 394, 292),
            text(506, 344, "consultation notes", size=9),
            text(
                350,
                420,
                "Exactly ONE Level 0 diagram per system. Every store is written by one process and read by another.",
                size=10,
                italic=True,
            ),
            text(
                350,
                435,
                "The clerk, the nurse and the administrator are inside the system: their work IS these processes.",
                size=10,
                italic=True,
            ),
        ]
    ),
    "The clinic Level 0 diagram: five numbered processes, three data stores and the four external agents. The prescription comes out of the consultation, process 3.0, which is where the doctor's notes arrive.",
    "Level 0 data flow diagram for the clinic with five numbered processes and three data stores",
)


# ============================================================== the use cases
def use_case_diagram(title, actors, cases, links, includes, w, h, note=None):
    body = [box(190, 40, 320, h - 90, "", bold=False), text(350, 60, title, bold=True, size=12)]
    for cx, cy, name in actors:
        body.append(actor(cx, cy, name))
    for cx, cy, name in cases:
        body.append(usecase(cx, cy, name))
    for x1, y1, x2, y2 in links:
        body.append(line(x1, y1, x2, y2, arrow=False))
    for x1, y1, x2, y2, label in includes:
        body.append(line(x1, y1, x2, y2, dashed=True))
        # beside the arrow, never across the oval it points at
        body.append(text((x1 + x2) / 2 + 44, (y1 + y2) / 2 + 4, label, size=9, italic=True))
    if note:
        body.append(text(w / 2, h - 14, note, size=10, italic=True))
    return "".join(body)


add(
    "sportscentre-usecase",
    700,
    450,
    use_case_diagram(
        "SPORTS CENTRE BOOKING SYSTEM",
        actors=[(60, 120, "Customer"), (640, 120, "Staff/Admin")],
        cases=[
            (350, 100, "Log In"),
            (350, 150, "View Facilities"),
            (350, 200, "Check Availability"),
            (350, 250, "Make Booking"),
            (350, 300, "Make Payment"),
            (350, 345, "Generate Reports"),
        ],
        links=[
            (78, 130, 274, 100),
            (78, 135, 274, 150),
            (78, 140, 274, 250),
            (622, 130, 426, 100),
            (622, 140, 426, 345),
        ],
        includes=[
            (330, 231, 330, 219, "include"),
            (350, 269, 350, 281, "include"),
        ],
        w=700,
        h=450,
        note="Make Booking INCLUDES Check Availability and Make Payment: always, every booking. Actors stay outside the boundary.",
    ),
    "The sports centre use case diagram. The boundary is drawn and labelled, both actors stand outside it, and Make Booking includes Check Availability and Make Payment, because both happen on every booking.",
    "Use case diagram for the sports centre booking system with Customer and Staff Admin actors",
)

add(
    "appointments-usecase",
    700,
    410,
    use_case_diagram(
        "CLINIC APPOINTMENTS SYSTEM",
        actors=[(60, 120, "Patient"), (640, 120, "Receptionist")],
        cases=[
            (350, 100, "Make Appointment"),
            (350, 150, "Change Appointment"),
            (350, 200, "Cancel Appointment"),
            (350, 250, "Verify Patient"),
            (350, 300, "Add Patient"),
        ],
        links=[
            (78, 125, 274, 100),
            (78, 130, 274, 150),
            (78, 135, 274, 200),
            (622, 130, 426, 100),
            (622, 140, 426, 300),
        ],
        includes=[
            (330, 231, 330, 119, "include"),
            (370, 281, 370, 269, "extend"),
        ],
        w=700,
        h=410,
        note="Verify Patient is an INCLUDE of every appointment use case. Add Patient EXTENDS it, only when the caller turns out to be new.",
    ),
    "The appointments use case diagram. Verifying the patient and their unpaid bills happens on every call, so it is an include; adding a new patient happens only sometimes, so it extends.",
    "Use case diagram for hospital appointments with Patient and Receptionist actors",
)

add(
    "hospital-billing-usecase",
    700,
    440,
    use_case_diagram(
        "PATIENT BILLING SYSTEM",
        actors=[(60, 130, "Patient"), (640, 90, "Nurse"), (640, 250, "Doctor")],
        cases=[
            (350, 100, "Enquire About Drugs"),
            (350, 150, "Check Vitals"),
            (350, 200, "Verify Insurance"),
            (350, 250, "Refer To Doctor"),
            (350, 300, "Advise On Drugs"),
            (350, 348, "Produce Bill"),
        ],
        links=[
            (78, 138, 274, 100),
            (78, 145, 274, 348),
            (622, 100, 426, 150),
            (622, 105, 426, 250),
            (622, 258, 426, 300),
        ],
        includes=[(330, 181, 330, 119, "include")],
        w=700,
        h=440,
        note="The Insurance Carrier is an EXTERNAL SERVER actor: it responds to the request from Verify Insurance. No insurance, no attendance.",
    ),
    "The patient billing use case diagram. Verifying insurance is an include of the enquiry, because the narrative says he will not be attended to without it, and the insurance carrier is an external server actor.",
    "Use case diagram for a hospital patient billing system with Patient, Nurse and Doctor actors",
)


def build():
    OUT.write_text(json.dumps(FIGURES, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for key, html in FIGURES.items():
        assert "currentColor" in html, key
        assert "aria-label" in html, key
        # currentColor only, so the figure works in both themes. The only # in a
        # figure is the arrow marker reference, url(#insarrow).
        assert not re.search(r"#[0-9a-fA-F]{3,6}", html), f"{key}: a hard coded colour"
    print(f"  {len(FIGURES)} figures drawn and parsed -> data/ins224/figures.json")
    for key in FIGURES:
        print(f"    {key}")


if __name__ == "__main__":
    build()
