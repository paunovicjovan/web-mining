import langextract as lx

EXTRACTION_EXAMPLES = [
    lx.data.ExampleData(
        text='The battery life on this phone is amazing and easily lasts two days, but the camera is a bit grainy in low light.',
        extractions=[
            lx.data.Extraction(extraction_class='aspect', extraction_text='battery life',
                               attributes={'sentiment': 'positive'}),
            lx.data.Extraction(extraction_class='aspect', extraction_text='camera',
                               attributes={'sentiment': 'negative'}),
        ]
    ),
    lx.data.ExampleData(
        text='The screen is vivid and very bright, though I find the charging speed to be average.',
        extractions=[
            lx.data.Extraction(extraction_class='aspect', extraction_text='screen',
                               attributes={'sentiment': 'positive'}),
            lx.data.Extraction(extraction_class='aspect', extraction_text='charging speed',
                               attributes={'sentiment': 'neutral'}),
        ]
    ),
    lx.data.ExampleData(
        text='Terrible speaker quality and the price is very high for what it offers.',
        extractions=[
            lx.data.Extraction(extraction_class='aspect', extraction_text='speaker quality',
                               attributes={'sentiment': 'negative'}),
            lx.data.Extraction(extraction_class='aspect', extraction_text='price',
                               attributes={'sentiment': 'negative'}),
        ]
    ),
    lx.data.ExampleData(
        text='The build quality is solid, much better than my old Samsung or the iPhone I used to have.',
        extractions=[
            lx.data.Extraction(extraction_class='aspect', extraction_text='build quality',
                               attributes={'sentiment': 'positive'}),
        ]
    )
]
