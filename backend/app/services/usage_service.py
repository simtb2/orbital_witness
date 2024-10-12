import requests
from fastapi import Depends
from datetime import datetime
from schemas.usage import Usage, UsageList
from schemas.message import Message
from schemas.report import Report
from utils.text_to_credits import TextToCredits
from utils.cache import Cache
from typing import Dict, List, Optional, Tuple
from configuration.config import config

class UsageService:
    def __init__(self):
        self.reports: Dict[int, Tuple[str, int]] = dict()
        self.cache: Cache = Cache()
        
    def get_usage_for_current_period(self) -> UsageList:
        usage_list: UsageList = self.cache.get('usage')
        
        if not usage_list:
            total_usage: List[Usage] = self.__get_total_usage()
            usage_list: UsageList = UsageList(usage=total_usage)
            self.cache.set('usage', usage_list)
        
        return usage_list

    def __get_total_usage(self) -> List[Usage]:
        current_period_url: str = f"{config.BASE_URL}/messages/current-period"
        response = requests.get(current_period_url)
        messages: Dict = response.json()['messages']
        usage: List[Usage] = self.__get_total_usage_helper(messages)
        
        return usage

    def __get_total_usage_helper(self, messages: Dict) -> List[Usage]:
        usage_list: List[Usage] = []
        
        for message in messages:
            current_message: Message = Message(**message)
            message_id: int = current_message.id
            timestamp: datetime = current_message.timestamp
            report_id: int = current_message.report_id
            usage_credit_cost: float = None
            
            if report_id:
                report_url: str = f"{config.BASE_URL}/reports/{report_id}"
                report_response: dict = requests.get(report_url)
                response_status_code: int = report_response.status_code
                
                if response_status_code == 200 and report_id not in self.reports:
                        report: Report = Report(**report_response.json())
                        report_credit_cost: float = report.credit_cost
                        report_name: str = report.name
                        self.reports[report_id] = (report_name, report_credit_cost)
                        usage_credit_cost = report_credit_cost
                        
                        usage = self.__create_usage(message_id, timestamp, usage_credit_cost, report_name)
                        usage_list.append(usage)
                        continue
            
            if not usage_credit_cost:
                text: str = current_message.text
                text_to_credits: float = TextToCredits(text).get_total_credits()
                usage_credit_cost = text_to_credits
            
            usage = self.__create_usage(message_id, timestamp, usage_credit_cost)
            usage_list.append(usage)
            
        return usage_list
    
    def __create_usage(self, message_id: int, timestamp: datetime, credits_used: int, report_name: Optional[str]=None) -> Usage:
        refortmated_datetime: str = timestamp.strftime("%d-%m-%Y %H:%M")
        return Usage(message_id=message_id, timestamp=refortmated_datetime, credits_used=credits_used, report_name=report_name)
