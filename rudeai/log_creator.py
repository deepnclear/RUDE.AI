"""
RUDE.AI: Inner processing Log and Override Engine
Log Creator - Creates structured logs from user situation descriptions
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from .log_format import StructuredLogFormat, LogStructure

class LogCreator:
    def __init__(self):
        self.somatic_patterns = self._load_somatic_patterns()
        self.trigger_patterns = self._load_trigger_patterns()
        self.insight_templates = self._load_insight_templates()
        
    def create_structured_log(self, situation_text: str, log_id: str) -> StructuredLogFormat:
        """Create a structured log from user situation description"""
        
        timestamp = datetime.now()
        
        # Generate header with date and natural time
        header = LogStructure.get_header_format(timestamp)
        
        # Extract components using pattern matching
        situation = self._extract_situation(situation_text)
        trigger = self._extract_trigger(situation_text)
        somatic_cognitive_response = self._extract_somatic_cognitive_response(situation_text)
        insight = self._generate_insight(situation_text, trigger, somatic_cognitive_response)
        
        return StructuredLogFormat(
            date=timestamp.strftime("%Y-%m-%d"),
            time_of_day=LogStructure.get_time_of_day(timestamp),
            header=header,
            situation=situation,
            trigger=trigger,
            somatic_cognitive_response=somatic_cognitive_response,
            insight=insight,
            log_id=log_id,
            timestamp=timestamp,
            raw_situation=situation_text
        )
    
    def format_log_for_confirmation(self, log: StructuredLogFormat) -> str:
        """Format the log for user confirmation"""
        
        formatted_log = f"""{log.header}

Situation: {log.situation}
Trigger: {log.trigger}
Somatic Cognitive Response: {log.somatic_cognitive_response}
Insight: {log.insight}"""
        
        return formatted_log
    
    def _extract_situation(self, text: str) -> str:
        """Extract situational context from user description"""
        text_lower = text.lower()
        
        # Look for activity patterns
        activity_patterns = [
            (r'while (?:talking to|speaking with|calling) (?:my )?(?:father|mother|sister|boss|colleague|friend)', 'communication'),
            (r'while (?:cooking|working|driving|eating|walking)', 'daily_activity'),
            (r'(?:paying|sending|receiving) (?:money|payment|rent|deposit)', 'financial_transaction'),
            (r'(?:interview|meeting|appointment|call) (?:with|at|for)', 'professional_interaction'),
            (r'at (?:work|home|office|gym|restaurant|meeting)', 'location_based'),
            (r'in (?:the|my) (?:kitchen|bedroom|car|office|meeting|gym)', 'location_based')
        ]
        
        # Find activity matches
        for pattern, category in activity_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return self._clean_and_capitalize(match.group())
        
        # Look for emotional situation patterns
        emotional_contexts = [
            r'had (?:a )?(?:fight|argument|conflict) with',
            r'received (?:a )?(?:message|call|email) from',
            r'decided (?:to|not to)',
            r'trying to (?:sell|buy|get|find)',
            r'need(?:ed)? to (?:go|do|get|make)'
        ]
        
        for pattern in emotional_contexts:
            match = re.search(pattern, text_lower)
            if match:
                # Extract surrounding context
                start_idx = max(0, match.start() - 20)
                end_idx = min(match.end() + 50, len(text))
                context = text[start_idx:end_idx].strip()
                return self._clean_and_capitalize(context)
        
        # Fallback: use first substantial sentence
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]
        if sentences:
            return self._clean_and_capitalize(sentences[0])
        
        return "Emotional situation requiring processing"
    
    def _extract_trigger(self, text: str) -> str:
        """Extract specific triggers from situation text"""
        text_lower = text.lower()
        
        # Primary trigger patterns from examples
        trigger_patterns = [
            # Internal voice patterns
            (r'internal voice.*?(?:saying|telling|about).*?(?:waste|stupid|should)', 'internal_voice'),
            (r'keep thinking (?:about|that).*?(?:stupid|waste|should|wrong)', 'internal_voice'),
            (r'voice.*?(?:saying|telling).*?["\']([^"\']*)["\']', 'internal_voice'),
            
            # Communication triggers
            (r'keep checking.*?(?:phone|message|email|status)', 'checking_compulsion'),
            (r'looking at.*?(?:phone|message|email).*?(?:times|hour)', 'checking_compulsion'), 
            (r'sent.*?(?:message|email|text).*?(?:checking|looking)', 'communication_trigger'),
            
            # Emotional state triggers
            (r'(?:anxiety|stress|worry|fear) about (?:the )?(?:money|cost|deadline|presentation)', 'anxiety_trigger'),
            (r'feeling (?:terrible|guilty|bad) (?:about|and)', 'emotional_trigger'),
            (r'(?:guilt|shame|anger) (?:sitting|mixed with)', 'emotional_trigger'),
            
            # Anticipatory triggers
            (r'(?:presentation|interview|meeting) (?:tomorrow|soon|coming)', 'performance_anxiety'),
            (r'woke up.*?(?:mind racing|thinking about|worrying)', 'anticipatory_worry'),
            (r'keep (?:reviewing|going over|thinking about).*?(?:notes|presentation|what)', 'preparation_anxiety')
        ]
        
        found_triggers = []
        
        for pattern, trigger_type in trigger_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # Find complete sentence containing the match
                sentences = text.split('.')
                trigger_context = None
                
                for sentence in sentences:
                    sentence_lower = sentence.lower().strip()
                    if any(word in sentence_lower for word in match.group().split()[:3]):
                        trigger_context = sentence.strip()
                        break
                
                # If no complete sentence found, extract with better boundaries
                if not trigger_context or len(trigger_context) < 10:
                    start_idx = max(0, match.start() - 10)
                    end_idx = min(match.end() + 50, len(text))
                    context = text[start_idx:end_idx].strip()
                    
                    # Find natural break points
                    for punct in ['. ', '! ', '? ', ' and ', ' but ', ' so ']:
                        if punct in context[20:]:  # Don't break too early
                            context = context[:context.find(punct, 20) + 1].strip()
                            break
                    
                    trigger_context = context
                
                if trigger_context and len(trigger_context) > 10:
                    found_triggers.append((trigger_context, trigger_type, len(trigger_context)))
        
        if found_triggers:
            # Select best trigger (prefer longer, more specific ones)
            best_trigger = max(found_triggers, key=lambda x: x[2])
            return self._clean_and_capitalize(best_trigger[0])
        
        # Fallback: look for emotional activation patterns
        fallback_patterns = [
            r'every time.*?(?:see|look|think).*?(?:feel|get)',
            r'(?:can\'t stop|keep).*?(?:myself|thinking|looking)',
            r'(?:woke up|started).*?(?:with|feeling).*?(?:racing|anxiety|stress)',
            r'(?:feel|feeling).*?(?:terrible|guilty|anxious|stressed)'
        ]
        
        for pattern in fallback_patterns:
            match = re.search(pattern, text_lower)
            if match:
                start_idx = max(0, match.start() - 5)
                end_idx = min(match.end() + 25, len(text))
                context = text[start_idx:end_idx].strip()
                return self._clean_and_capitalize(context)
        
        return self._extract_emotional_context(text)
    
    def _extract_somatic_cognitive_response(self, text: str) -> str:
        """Extract physical/bodily reactions and cognitive responses from text"""
        text_lower = text.lower()
        
        # Somatic indicators organized by body system
        somatic_patterns = {
            'chest': [
                r'chest.*?(?:tight|heavy|burning|explosion|tension|pressure)',
                r'(?:micro|atomic) (?:ball|bomb) explosion.*?(?:chest|breast)',
                r'burning.*?(?:chest|breast)',
                r'(?:light|heavy) (?:burning|pressure).*?chest'
            ],
            'breathing': [
                r'breathing.*?(?:shallow|heavy|difficult|short)',
                r'can\'?t breathe',
                r'breath.*?(?:short|shallow|racing)',
                r'holding.*?breath'
            ],
            'heart': [
                r'heart.*?(?:racing|pounding|beating|fast)',
                r'heart rate.*?(?:up|elevated|increased)'
            ],
            'nervous_system': [
                r'(?:sympathetic|somatic) (?:reflex|spike|response|activation)',
                r'nervous.*?(?:reaction|response|energy)',
                r'(?:anxiety|stress) (?:pulse|spike|wave)',
                r'startle.*?response'
            ],
            'muscular': [
                r'(?:hands|fingers).*?(?:shaking|trembling|tense)',
                r'(?:jaw|shoulders|muscles).*?(?:clenched|tight|tense)',
                r'shoulders.*?(?:raised|hunched|tense)'
            ],
            'digestive': [
                r'stomach.*?(?:knots|tight|churning|dropping)',
                r'nauseous|nausea',
                r'(?:esophageal )?reflux',
                r'(?:bowel|defecated).*?(?:activity|movement|times)'
            ],
            'cognitive': [
                r'thoughts?.*?(?:racing|spinning|looping)',
                r'mental.*?(?:loop|hoarding|checking)',
                r'obsessive.*?(?:checking|thoughts)',
                r'cognitive.*?(?:strain|load)'
            ]
        }
        
        found_responses = []
        
        for body_system, patterns in somatic_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    # Clean and add matches
                    for match in matches:
                        if isinstance(match, tuple):
                            match = ' '.join(match)
                        cleaned_match = self._clean_somatic_cognitive_response(match)
                        if cleaned_match:
                            found_responses.append(cleaned_match)
        
        # Look for intensity descriptors
        intensity_patterns = [
            r'(?:mild|light|slight) (?:anxiety|discomfort|tension|burning)',
            r'(?:intense|strong|heavy|overwhelming) (?:feeling|sensation|response)',
            r'(?:immediate|sudden|instant) (?:reaction|response|feeling)'
        ]
        
        for pattern in intensity_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                found_responses.extend([self._clean_somatic_cognitive_response(match) for match in matches])
        
        if found_responses:
            # Remove duplicates and filter out poor quality responses
            unique_responses = []
            seen = set()
            for response in found_responses:
                cleaned = response.strip()
                if (len(cleaned) > 5 and 
                    cleaned.lower() not in seen and
                    not cleaned.startswith('and ') and
                    len(cleaned.split()) > 1):  # Must be more than one word
                    unique_responses.append(cleaned)
                    seen.add(cleaned.lower())
            
            # Format as single item or bullet points
            if len(unique_responses) == 1:
                return unique_responses[0].capitalize()
            elif len(unique_responses) > 1:
                # Use bullet points with dashes (–) like in examples
                formatted = '\n'.join([f"– {response.capitalize()}" for response in unique_responses[:4]])
                return formatted
        
        return "Emotional activation detected"
    
    def _generate_insight(self, text: str, trigger: str, somatic_cognitive_response: str) -> str:
        """Generate insight based on patterns identified in the situation"""
        text_lower = text.lower()
        
        # Identify pattern types from examples with better scoring
        pattern_indicators = {
            'sunk_cost': ['money', 'cost', 'waste', 'spent', 'paid', 'dollar', 'price', 'expensive', 'wasted', 'stupid'],
            'anticipatory_vigilance': ['checking', 'message', 'phone', 'read', 'delivered', 'status', 'response', 'looked', 'times'],
            'emotional_pendulum': ['anger', 'guilt', 'reconcil', 'reach out', 'apologize', 'sorry', 'conflict', 'argument', 'fight'],
            'compliance_reflex': ['thank', 'grateful', 'obliged', 'should', 'have to', 'need to', 'supposed to'],
            'boundary_violation': ['interrupt', 'unexpected', 'unannounced', 'without', 'permission', 'suddenly'],
            'performance_anxiety': ['presentation', 'interview', 'meeting', 'tomorrow', 'performance', 'speak', 'present', 'woke up', 'mind racing'],
            'family_dynamics': ['father', 'mother', 'sister', 'parent', 'family', 'relative'],
            'financial_anxiety': ['payment', 'transaction', 'money', 'bank', 'deposit', 'transfer']
        }
        
        # Count pattern matches
        pattern_scores = {}
        for pattern_name, keywords in pattern_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                pattern_scores[pattern_name] = score
        
        # Generate insight based on strongest pattern
        if pattern_scores:
            primary_pattern = max(pattern_scores, key=pattern_scores.get)
            return self._generate_pattern_insight(primary_pattern, text, trigger, somatic_cognitive_response)
        
        # Generic insight for unclassified patterns
        return self._generate_generic_insight(text, somatic_cognitive_response)
    
    def _generate_pattern_insight(self, pattern_type: str, text: str, trigger: str, somatic_cognitive_response: str) -> str:
        """Generate specific insights based on identified patterns"""
        
        if pattern_type == 'sunk_cost':
            return ("The emotional response is not about the specific cost—it's a proxy for "
                   "inherited expectations of self-punishment when resources are perceived as wasted. "
                   "Your system conflates monetary loss with personal failure. "
                   "Nothing is wasted if it protects your nervous system equilibrium.")
        
        elif pattern_type == 'anticipatory_vigilance':
            return ("This demonstrates anticipatory vigilance: monitoring external responses "
                   "as a form of emotional control and self-protection. "
                   "The checking behavior substitutes action for outcome certainty. "
                   "You are building internal equilibrium rather than outsourcing it to others' responses.")
        
        elif pattern_type == 'emotional_pendulum':
            return ("This shows the emotional pendulum—intensity swings between rupture and repair. "
                   "The guilt impulse functions as an attempt to restore connection at the cost of boundary integrity. "
                   "Anger creates illusion of power; guilt creates illusion of restoration. "
                   "Together they form a loop that avoids authentic processing.")
        
        elif pattern_type == 'compliance_reflex':
            return ("This is autonomic compliance reflex. Your system registers temporary relief "
                   "as relationship repair, bypassing the original boundary breach. "
                   "When gratitude overrides memory or caution, it becomes compulsive appeasement. "
                   "True appreciation does not require abandoning discernment.")
        
        elif pattern_type == 'boundary_violation':
            return ("Gratitude became behavioral residue from past boundary breaches—"
                   "an overcompensation strategy for discomfort in asymmetric exchanges. "
                   "The system learned to convert boundary violations into obligations. "
                   "Assistance offered without consent does not create emotional debt.")
        
        elif pattern_type == 'performance_anxiety':
            return ("Your nervous system is executing anticipatory preparation protocol—"
                   "clearing system load before performance exposure. "
                   "The body treats upcoming evaluation as survival-level importance. "
                   "Anxiety here functions as signal preparing for performance, not malfunction. "
                   "You are monitoring the machinery, not being overwhelmed by it.")
        
        elif pattern_type == 'family_dynamics':
            return ("This interaction carries emotional lineage charge—expectation, wound, "
                   "and historic patterns converge in family communications. "
                   "The body holds inherited scripts about approval and disappointment. "
                   "Present moment autonomy requires separation from ancestral emotional programming.")
        
        elif pattern_type == 'financial_anxiety':
            return ("Financial transactions trigger precision anxiety—the nervous system "
                   "treats monetary accuracy as survival-level importance. "
                   "Mental hoarding accumulates micro-anxieties without purge. "
                   "Precision is not panic. Every cent does not cost your peace.")
        
        else:
            return self._generate_generic_insight(text, somatic_cognitive_response)
    
    def _generate_generic_insight(self, text: str, somatic_cognitive_response: str) -> str:
        """Generate generic insight when no specific pattern is identified"""
        
        if any(word in somatic_cognitive_response.lower() for word in ['chest', 'explosion', 'burning']):
            return ("This was a somatic override scenario. Your nervous system misread the situation "
                   "as threat based on prior emotional scripts. "
                   "The body's response preceded cognitive evaluation. "
                   "Recognition interrupts the automatic sequence.")
        
        elif any(word in somatic_cognitive_response.lower() for word in ['anxiety', 'nervous', 'stress']):
            return ("Anxiety functions here as anticipatory protection—attempting to control "
                   "uncertain outcomes through mental preparation. "
                   "The nervous system conflates vigilance with safety. "
                   "Present moment awareness dissolves future-based threat assessment.")
        
        else:
            return ("Emotional activation occurred through learned response patterns. "
                   "The reaction stems from historical associations rather than present circumstances. "
                   "Conscious recognition creates space between trigger and response. "
                   "Pattern awareness prevents automatic behavioral discharge.")
    
    def _clean_and_capitalize(self, text: str) -> str:
        """Clean and format text consistently"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        # Capitalize first letter
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
        return cleaned
    
    def _clean_somatic_cognitive_response(self, text: str) -> str:
        """Clean somatic cognitive response text"""
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', text.strip())
        # Remove common filler words
        cleaned = re.sub(r'\b(?:like|you know|kind of|sort of)\b', '', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _extract_emotional_context(self, text: str) -> str:
        """Extract emotional context as fallback trigger"""
        emotional_words = {
            'anxiety': ['anxious', 'worried', 'nervous', 'stress', 'panic'],
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'irritated'],
            'guilt': ['guilty', 'shame', 'ashamed', 'embarrassed'],
            'fear': ['scared', 'afraid', 'fearful', 'terrified'],
            'sadness': ['sad', 'depressed', 'down', 'hopeless']
        }
        
        text_lower = text.lower()
        
        for emotion, variants in emotional_words.items():
            if any(variant in text_lower for variant in variants):
                return f"Emotional activation involving {emotion} response pattern"
        
        return "Internal emotional response activation"
    
    def _load_somatic_patterns(self) -> Dict[str, List[str]]:
        """Load somatic response patterns from examples"""
        return {
            'chest_reactions': [
                'chest tight', 'chest heavy', 'chest burning', 'micro ball explosion',
                'atomic bomb explosion', 'light burning', 'presence in chest'
            ],
            'anxiety_responses': [
                'mild anxiety', 'light anxiety', 'anxiety pulse', 'sympathetic spike',
                'sympathetic reflex', 'somatic reflex', 'nervous reaction'
            ],
            'physical_symptoms': [
                'hands shaking', 'heart racing', 'breathing shallow', 'muscle tension',
                'jaw clenched', 'shoulders raised', 'stomach knots', 'reflux'
            ]
        }
    
    def _load_trigger_patterns(self) -> Dict[str, List[str]]:
        """Load trigger patterns from examples"""
        return {
            'financial_triggers': [
                'money', 'cost', 'waste', 'spent', 'payment', 'transaction', 'price'
            ],
            'communication_triggers': [
                'message', 'call', 'phone', 'email', 'text', 'checking', 'read'
            ],
            'interpersonal_triggers': [
                'conflict', 'argument', 'guilt', 'anger', 'relationship', 'father', 'mother'
            ],
            'performance_triggers': [
                'interview', 'meeting', 'late', 'time pressure', 'deadline', 'appointment'
            ]
        }
    
    def _load_insight_templates(self) -> Dict[str, str]:
        """Load insight templates based on pattern analysis"""
        return {
            'sunk_cost': "The {emotion} is not about the {object}—it's a proxy for inherited expectations",
            'vigilance': "This demonstrates anticipatory vigilance: {behavior} as emotional control",
            'pendulum': "This shows the emotional pendulum—intensity swings between {state1} and {state2}",
            'compliance': "This is autonomic compliance reflex: {trigger} creates obligation pressure",
            'boundary': "This interaction carries {dynamic}—{pattern} converges in {context}"
        }