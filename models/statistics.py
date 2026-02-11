"""
Statistics Engine - výpočty statistik z dat
"""

from datetime import datetime, timedelta
import os
import pickle


class Statistics:
    """
    Počítá statistiky z tasků, goals a cyklů
    """
    
    def __init__(self, cycles_manager, all_tasks, goals):
        self.cycles_manager = cycles_manager
        self.all_tasks = all_tasks
        self.goals = goals
    
    # ===== HELPER METHODS =====
    
    def get_tasks_for_period(self, period="current_week"):
        """
        Vrátí tasky pro dané období
        
        Args:
            period: "current_week" | "last_6_weeks" | "current_cycle" | "all_time"
        
        Returns:
            list: Filtrované tasky
        """
        active_cycle = self.cycles_manager.get_active_cycle()
        
        if not active_cycle:
            return []
        
        now = datetime.now()
        start_date = active_cycle['start_date']
        
        # Vypočítej hranice období
        if period == "current_week":
            # Aktuální týden cyklu
            days_since_start = (now - start_date).days
            current_week = (days_since_start // 7) + 1
            week_offset = (current_week - 1) * 7
            period_start = start_date + timedelta(days=week_offset)
            period_end = period_start + timedelta(days=7)
        
        elif period == "last_6_weeks":
            # Posledních 6 týdnů
            period_start = now - timedelta(days=42)  # 6 týdnů = 42 dní
            period_end = now
        
        elif period == "current_cycle":
            # Celý aktivní cyklus
            period_start = start_date
            period_end = active_cycle['end_date']
        
        elif period == "all_time":
            # Všechny cykly (aktivní + archivované)
            return self._get_all_time_tasks()
        
        else:
            return []
        
        # Filtruj tasky podle data
        filtered_tasks = []
        for task in self.all_tasks.list_of_all_tasks_objects:
            task_date = task[2]
            
            if isinstance(task_date, datetime):
                task_date_only = task_date.date()
            else:
                task_date_only = task_date
            
            period_start_date = period_start.date() if isinstance(period_start, datetime) else period_start
            period_end_date = period_end.date() if isinstance(period_end, datetime) else period_end
            
            if period_start_date <= task_date_only < period_end_date:
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def _get_all_time_tasks(self):
        """
        Vrátí tasky ze všech cyklů (aktivní + archivované)
        """
        all_tasks = []
        
        # Aktivní cyklus
        all_tasks.extend(self.all_tasks.list_of_all_tasks_objects)
        
        # Archivované cykly
        cycles = self.cycles_manager.get_all_cycles_summary()
        
        for cycle in cycles:
            if cycle['status'] == 'completed':
                archive_file = cycle.get('archive_file')
                if archive_file:
                    archive_path = os.path.join(self.cycles_manager.archive_dir, archive_file)
                    
                    if os.path.exists(archive_path):
                        with open(archive_path, 'rb') as f:
                            archive_data = pickle.load(f)
                            tasks_df = archive_data.get('tasks')
                            
                            if tasks_df is not None:
                                all_tasks.extend(tasks_df.values.tolist())
        
        return all_tasks
    
    def get_tasks_by_category(self, tasks, category):
        """
        Filtruje tasky podle kategorie (subclass)
        """
        return [t for t in tasks if t[1] == category]
    
    def get_reviewed_tasks(self, tasks):
        """
        Vrátí jen tasky které mají review
        """
        reviewed = []
        for task in tasks:
            if len(task) > 4 and task[4] is not None:  # Má score
                reviewed.append(task)
        return reviewed
    
    # ===== OVERVIEW STATS =====
    
    def get_overview_stats(self, period="current_week"):
        """
        Celkové statistiky pro dané období
        
        Returns:
            dict: {
                'total_tasks': int,
                'total_hours': float,
                'avg_score': float,
                'reviewed_count': int,
                'review_rate': float (%)
            }
        """
        tasks = self.get_tasks_for_period(period)
        reviewed = self.get_reviewed_tasks(tasks)
        
        total_tasks = len(tasks)
        total_hours = sum(t[3] for t in tasks)  # sum of hours
        
        # Průměrné score (jen z reviewed tasků)
        if reviewed:
            avg_score = sum(t[4] for t in reviewed) / len(reviewed)
        else:
            avg_score = 0.0
        
        reviewed_count = len(reviewed)
        review_rate = (reviewed_count / total_tasks * 100) if total_tasks > 0 else 0.0
        
        return {
            'total_tasks': total_tasks,
            'total_hours': total_hours,
            'avg_score': round(avg_score, 1),
            'reviewed_count': reviewed_count,
            'review_rate': round(review_rate, 1)
        }
    
    # ===== CATEGORY STATS =====
    
    def get_category_stats(self, period="current_week"):
        """
        Statistiky podle kategorií
        
        Returns:
            list: [
                {
                    'category': str,
                    'tasks_count': int,
                    'hours': float,
                    'avg_score': float,
                    'review_rate': float,
                    'goal_target': float or None,
                    'trend': float (rozdíl oproti předchozímu období)
                },
                ...
            ]
        """
        tasks = self.get_tasks_for_period(period)
        
        # Získej všechny unikátní kategorie
        categories = list(set(t[1] for t in tasks if t[1]))  # subclass
        
        stats = []
        
        for category in categories:
            cat_tasks = self.get_tasks_by_category(tasks, category)
            cat_reviewed = self.get_reviewed_tasks(cat_tasks)
            
            tasks_count = len(cat_tasks)
            hours = sum(t[3] for t in cat_tasks)
            
            if cat_reviewed:
                avg_score = sum(t[4] for t in cat_reviewed) / len(cat_reviewed)
            else:
                avg_score = 0.0
            
            review_rate = (len(cat_reviewed) / tasks_count * 100) if tasks_count > 0 else 0.0
            
            # Najdi goal pro tuto kategorii
            goal_target = self._get_goal_target_for_category(category)
            
            # Spočítej trend (porovnání s předchozím obdobím)
            trend = self._calculate_trend(category, period)
            
            stats.append({
                'category': category,
                'tasks_count': tasks_count,
                'hours': round(hours, 1),
                'avg_score': round(avg_score, 1),
                'review_rate': round(review_rate, 1),
                'goal_target': goal_target,
                'trend': round(trend, 1)
            })
        
        # Seřaď podle avg_score (nejlepší první)
        stats.sort(key=lambda x: x['avg_score'], reverse=True)
        
        return stats
    
    def _get_goal_target_for_category(self, category):
        """
        Najde goal target score pro danou kategorii
        """
        active_cycle = self.cycles_manager.get_active_cycle()
        
        if not active_cycle:
            return None
        
        cycle_start = active_cycle['start_date']
        
        # Najdi goals pro aktuální cyklus
        for goal in self.goals.list_of_all_goals_objects:
            if len(goal) < 8:
                continue
            
            goal_category = goal[1]  # subclass
            goal_date = goal[4]  # date_of_creation
            goal_target = goal[3]  # average_score
            
            # Je to goal pro tuto kategorii a aktuální cyklus?
            if goal_category == category:
                if isinstance(goal_date, datetime):
                    goal_date = goal_date.date()
                
                cycle_start_date = cycle_start.date() if isinstance(cycle_start, datetime) else cycle_start
                
                if goal_date == cycle_start_date:
                    return goal_target
        
        return None
    
    def _calculate_trend(self, category, current_period):
        """
        Spočítá trend (rozdíl oproti předchozímu období)
        """
        # Pro jednoduchost: porovnej s předchozím stejně dlouhým obdobím
        current_tasks = self.get_tasks_by_category(
            self.get_tasks_for_period(current_period), 
            category
        )
        current_reviewed = self.get_reviewed_tasks(current_tasks)
        
        if not current_reviewed:
            return 0.0
        
        current_avg = sum(t[4] for t in current_reviewed) / len(current_reviewed)
        
        # TODO: Implementuj porovnání s předchozím obdobím
        # Pro teď vrátíme 0 (žádný trend)
        
        return 0.0
    
    # ===== BEST/WORST PERFORMERS =====
    
    def get_best_categories(self, period="current_week", limit=3):
        """
        Vrátí top N kategorií podle avg_score
        """
        stats = self.get_category_stats(period)
        return stats[:limit]  # Už seřazené
    
    def get_worst_categories(self, period="current_week", limit=3):
        """
        Vrátí bottom N kategorií podle avg_score
        """
        stats = self.get_category_stats(period)
        
        # Filtruj jen ty co mají nějaké reviewed tasky
        with_reviews = [s for s in stats if s['avg_score'] > 0]
        
        # Seřaď od nejhoršího
        with_reviews.sort(key=lambda x: x['avg_score'])
        
        return with_reviews[:limit]
    
    # ===== GOALS PROGRESS =====
    
    def get_goals_progress(self):
        """
        Vrátí progress pro všechny goals aktuálního cyklu
        
        Returns:
            list: [
                {
                    'goal_name': str,
                    'category': str,
                    'target_hours': float,
                    'actual_hours': float,
                    'target_score': float,
                    'actual_score': float,
                    'progress_percent': float,
                    'status': 'on_track' | 'behind' | 'exceeding'
                },
                ...
            ]
        """
        active_cycle = self.cycles_manager.get_active_cycle()
        
        if not active_cycle:
            return []
        
        cycle_start = active_cycle['start_date']
        cycle_start_date = cycle_start.date() if isinstance(cycle_start, datetime) else cycle_start
        
        goals_progress = []
        
        # Projdi všechny goals aktuálního cyklu
        for goal in self.goals.list_of_all_goals_objects:
            if len(goal) < 8:
                continue
            
            goal_date = goal[4]  # date_of_creation
            
            if isinstance(goal_date, datetime):
                goal_date = goal_date.date()
            
            # Je to goal aktuálního cyklu?
            if goal_date != cycle_start_date:
                continue
            
            goal_name = goal[0]
            category = goal[1]
            target_hours = goal[2]
            target_score = goal[3]
            
            # Získej tasky pro tento goal (kategorie + aktuální cyklus)
            cycle_tasks = self.get_tasks_for_period("current_cycle")
            goal_tasks = self.get_tasks_by_category(cycle_tasks, category)
            goal_reviewed = self.get_reviewed_tasks(goal_tasks)
            
            # Spočítej actual
            actual_hours = sum(t[3] for t in goal_tasks)
            
            if goal_reviewed:
                actual_score = sum(t[4] for t in goal_reviewed) / len(goal_reviewed)
            else:
                actual_score = 0.0
            
            # Progress
            progress_percent = (actual_hours / target_hours * 100) if target_hours > 0 else 0.0
            
            # Status
            if progress_percent >= 100 and actual_score >= target_score:
                status = 'exceeding'
            elif progress_percent >= 80 and actual_score >= target_score * 0.9:
                status = 'on_track'
            else:
                status = 'behind'
            
            goals_progress.append({
                'goal_name': goal_name,
                'category': category,
                'target_hours': target_hours,
                'actual_hours': round(actual_hours, 1),
                'target_score': target_score,
                'actual_score': round(actual_score, 1),
                'progress_percent': round(progress_percent, 1),
                'status': status
            })
        
        return goals_progress
    
    # ===== TRENDS DATA =====
    
    def get_score_trend_per_week(self):
        """
        Vrátí průměrné score po týdnech (pro graf)
        
        Returns:
            list: [(week_number, avg_score), ...]
        """
        active_cycle = self.cycles_manager.get_active_cycle()
        
        if not active_cycle:
            return []
        
        start_date = active_cycle['start_date']
        trend_data = []
        
        for week in range(1, 13):  # 12 týdnů
            week_start = start_date + timedelta(days=(week - 1) * 7)
            week_end = week_start + timedelta(days=7)
            
            # Získej tasky pro tento týden
            week_tasks = []
            for task in self.all_tasks.list_of_all_tasks_objects:
                task_date = task[2]
                
                if isinstance(task_date, datetime):
                    task_date = task_date.date()
                
                week_start_date = week_start.date() if isinstance(week_start, datetime) else week_start
                week_end_date = week_end.date() if isinstance(week_end, datetime) else week_end
                
                if week_start_date <= task_date < week_end_date:
                    week_tasks.append(task)
            
            # Spočítaj průměrné score
            reviewed = self.get_reviewed_tasks(week_tasks)
            
            if reviewed:
                avg_score = sum(t[4] for t in reviewed) / len(reviewed)
            else:
                avg_score = 0.0
            
            trend_data.append((week, round(avg_score, 1)))
        
        return trend_data
    
    def get_hours_per_week(self):
        """
        Vrátí celkové hodiny po týdnech (pro bar chart)
        
        Returns:
            list: [(week_number, total_hours), ...]
        """
        active_cycle = self.cycles_manager.get_active_cycle()
        
        if not active_cycle:
            return []
        
        start_date = active_cycle['start_date']
        hours_data = []
        
        for week in range(1, 13):
            week_start = start_date + timedelta(days=(week - 1) * 7)
            week_end = week_start + timedelta(days=7)
            
            # Získej tasky pro tento týden
            week_tasks = []
            for task in self.all_tasks.list_of_all_tasks_objects:
                task_date = task[2]
                
                if isinstance(task_date, datetime):
                    task_date = task_date.date()
                
                week_start_date = week_start.date() if isinstance(week_start, datetime) else week_start
                week_end_date = week_end.date() if isinstance(week_end, datetime) else week_end
                
                if week_start_date <= task_date < week_end_date:
                    week_tasks.append(task)
            
            total_hours = sum(t[3] for t in week_tasks)
            hours_data.append((week, round(total_hours, 1)))
        
        return hours_data