#include <helpers.hpp>

std::vector<std::string> convert_job_string_to_vector(const std::string &job_definition, const char delimiter)
{
	std::string token;
	std::vector<std::string> tokens;
	std::istringstream tokenStream(job_definition);

	std::string multitoken {};
	bool is_multitoken {false};
	while(std::getline(tokenStream, token, delimiter))
	{
		if (token.front() == '\'')
		{
			is_multitoken = true;
		}

		if (is_multitoken)
		{
			multitoken +=  multitoken.empty() ? token : " " + token;
			if (token.back() == '\'')
			{
				is_multitoken = false;
				token = multitoken;
				multitoken.clear();
			}
		}
		if (!is_multitoken)
		{
			tokens.push_back(token);
		}
	}
	return tokens;
}

Job::Job(std::vector<std::string> job_definition)
{
	this->job_params = job_definition.back();
	job_definition.pop_back();
	this->job_program = job_definition.back();
	job_definition.pop_back();

	this->day_of_week = job_definition.back();
	job_definition.pop_back();
	this->month = job_definition.back();
	job_definition.pop_back();
	this->month_day = job_definition.back();
	job_definition.pop_back();
	this->hours = job_definition.back();
	job_definition.pop_back();
	this->minutes = job_definition.back();
	job_definition.pop_back();
}

void Job::call_job()
{
	std::cout<<"Calling job: " <<this->job_program <<" " << this->job_params;
}


bool Job::is_minutes(const std::string min)
{
	return this->minutes != "*" ? min == this->minutes : true;
}

bool Job::is_hours(const std::string h)
{
	return this->hours != "*" ? h == this->hours : true;
}

bool Job::is_month_day(const std::string md)
{
	return this->month_day != "*" ?  md == this->month_day : true;
}

bool Job::is_month(const std::string m)
{
	return this->month != "*" ?  m == this->month : true;
}

bool Job::is_day_of_week(const std::string dow)
{
	return this->day_of_week != "*" ?  dow == this->day_of_week : true;
}

bool Job::is_time(const std::string t)
{
	auto time_vector = convert_job_string_to_vector(t, ':');
	return this->is_hours(time_vector.at(0)) && this->is_minutes(time_vector.at(1));
}

std::ostream& operator <<(std::ostream &out, const Job &j)
{
	out<<j.minutes <<" " <<j.hours <<" " <<j.month_day <<" " <<j.month <<" " <<j.day_of_week
		<<" " <<j.job_program <<" " <<j.job_params;
		return out;
}