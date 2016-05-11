#include "resources.h"
#include "tree.h"
#include "threads.h"

bool request_received_pulse = false;
bool download_complete = true;
#pragma zoom C1: LTL: G(!request_received_pulse U download_complete)

int total_left = 0;

void download_subtree(tree node) {
	job J = network_resources.schedule_download(node.url);
	J.wait();

	total_left --;
	if (total_left == 0)
		download_complete = true;

	vector<tree> ch = node.children();
	for(tree::iterator it = ch.begin(); it != ch.end(); it++) {
		spawn_thread(download_subtree, *it);
	}
}


void donwload_data(tree request) {
	#pragma zoom Enable C1

	// creating a pulse
	request_received_pulse = true;
	request_received_pulse = false;

	total_left = request.size();
	download_complete = false;

	spawn_thread(download_subtree, request);

}