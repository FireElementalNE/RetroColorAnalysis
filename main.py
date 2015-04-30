import argparse
from retro_analysis import analyze_image
from globals.global_values import INPUT_MODE
from globals.global_values import OUTPUT_MODE
from html_builder.html_builder import build_html

def run_main(game_name):
	input_done = analyze_image(game_name, INPUT_MODE, False)
	if input_done:
		output_done = analyze_image(game_name, OUTPUT_MODE, False)
		if output_done:
			html_done = build_html(game_name)
			

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Wrapper function')
	parser.add_argument('-g', '--game', help='Game name', required=True)
	args = parser.parse_args()
	run_main(args.game)