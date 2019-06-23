#include <iostream>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> convert_job_string_to_vector(const std::string &job_definition, const char delimiter = ' ');

class Job {
public:
	std::string minutes;
	std::string hours;
	std::string month_day;
	std::string month;
	std::string day_of_week;

	std::string job_program;
	std::string job_params;

	Job(std::vector<std::string> job_definition);
	void call_job();

	bool is_minutes(const std::string &min);
	bool is_hours(const std::string &h);
	bool is_month_day(const std::string &md);
	bool is_month(const std::string &m);
	bool is_day_of_week(const std::string &dow);
	bool is_time(const std::string &t);

	friend std::ostream& operator <<(std::ostream &out, const Job &j);
};
