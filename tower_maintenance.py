
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE towers (id INTEGER PRIMARY KEY, site TEXT, last_service INTEGER, faults INTEGER)")



def addTower(site, last_service, faults=0):
    conn.execute(
        """
        INSERT INTO towers (site, last_service, faults)
        VALUES (?, ?, ?)
        """,
        (site, last_service, faults),
    )
    conn.commit()

def serviceTower(tower_id, year):
    """Record tower servicing and report whether it succeeded."""
    try:
        cursor = conn.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        conn.commit()
    except sqlite3.Error:
        print("Service failed because of a database error.")
        return False

    if cursor.rowcount == 0:
        print(f"No tower found with ID {tower_id}.")
        return False

    return True


def overdue(year):
    rows = conn.execute("SELECT site, last_service FROM towers").fetchall()
    result = []
    for site, last in rows:
        if year - last >= 2:
            result.append(site)
    return result


def riskLevel(tower_id):
    """Return the risk level for a tower."""
    row = conn.execute(
        "SELECT faults FROM towers WHERE id = ?",
        (tower_id,),
    ).fetchone()

    if row is None:
        return "unknown"

    if row[0] > 3:
        return "high"

    return "normal"


def snapshot():
    return conn.execute("SELECT * FROM towers").fetchall()


def main():
    """Run a demonstration of the tower maintenance tracker."""
    addTower("Ridge-A", 2021, 5)
    addTower("Coast-B", 2024)

    service_count = int(serviceTower(2, 2025))
    total = len(snapshot())

    print(overdue(2025), riskLevel(1), total, service_count)


if __name__ == "__main__":
    main()

