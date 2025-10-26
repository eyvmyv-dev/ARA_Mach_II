    def _check_patterns(self, text: str, patterns: List[str]) -> float:
        """Check text against patterns and return confidence score."""
        if not text:
            return 0.0
            
        text = text.lower()
        confidence = 0.0
        
        for pattern in patterns:
            try:
                if re.search(fr'\b{pattern}\b', text, re.IGNORECASE):
                    confidence += 0.4
                    # Bonus for exact matches
                    if re.search(fr'^\s*{pattern}\s*$', text, re.IGNORECASE):
                        confidence += 0.2
            except re.error:
                # Skip invalid patterns
                continue
                
        # Add context confidence
        if self.industry == 'FACILITY':
            if re.search(r'(monthly|quarterly|annual|weekly)\s+pm', text, re.IGNORECASE):
                confidence += 0.1
            if re.search(r'building|facility|terminal|floor', text, re.IGNORECASE):
                confidence += 0.1
                
        return min(confidence, 1.0)