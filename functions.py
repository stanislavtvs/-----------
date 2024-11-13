import aiosqlite


class DataBaseInterface:
    def __init__(self):
        self.connection = None
        self.cursor = None

    async def connect(self, db_file: str) -> None:
        self.connection = await aiosqlite.connect("data.db")
        
    async def create_tables(self) -> None:
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
                user_id INTEGER,
                contact_name VARCHAR(128),
                contact VARCHAR(128)
            )
        """)
        await self.connection.commit()

    async def add_contact(self, user_id: int, contact_name: str, contact: str) -> None:
        await self.connection.execute("""
            INSERT INTO contacts
            VALUES (?, ?, ?)
        """, (user_id, contact_name, contact))
        await self.connection.commit()

    async def get_contacts(self, user_id: int) -> list[tuple[str, str]]:
        async with self.connection.execute("""
            SELECT contact_name, contact
            FROM contacts
            WHERE user_id=?
        """, (user_id,)) as cursor:
            return await cursor.fetchall()
