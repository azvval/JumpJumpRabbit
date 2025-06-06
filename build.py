import pygbag
import asyncio

async def build_game():
    """
    Oyunu web için build eder
    """
    # Pygbag ile build
    pygbag.run(
        main="main.py",
        name="Jump Jump Rabbit",
        title="Jump Jump Rabbit",
        author="Azra Şevval Küpeli, Ceren Eroğlu",
        icon="./assets/Idle1.png",  # Eğer varsa
        template="custom",
        width=400,
        height=700,
        assets_folder="assets/"
    )

if __name__ == "__main__":
    asyncio.run(build_game())