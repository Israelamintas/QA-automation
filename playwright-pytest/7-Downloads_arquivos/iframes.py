def test_iframe(page):
    page.goto("https://www.w3schools.com/html/tryit.asp?filename=tryhtml_iframe")
    page.pause()
    page.wait_for_load_state("domcontentloaded")

    iframe = page.frame_locator("#iframeResult")

    inner_iframe = iframe.frame_locator('[src="demo_iframe.htm"]')

    titulo = inner_iframe.locator("h1").inner_text()
    print("Texto dentro do iframe:", titulo)
