function labB = getClassNew(xData,classifs,mode)


    classvec=[0 0 0];
	margvec = [0 0 0];
	for i=1:3
		margvec(i) = classifs{i}.w'*xData'+classifs{i}.b;
		classvec(i) = sign(classifs{i}.w'*xData'+classifs{i}.b);
	end
    %%% truth table
	% 1 vs 2    1   -1   ? 
    % 2 vs 3    ?    1   -1 
    % 1 vs 3    1    ?   -1
   if mode ==1 % one vs one  
      labB = -1;
      if (classvec(1)>0 && classvec(3)>0) % minind(1)==1
          labB=1;
      end
      if (classvec(1)<0 && classvec(2)>0) % minind(1)==2
          labB=2;
      end
      if (classvec(2)<0 && classvec(3)<0) % minind(1)==3
          labB=3;
      end
  end
  if mode == 2 % one vs all
      labB=-1;
      if (classvec(3)<0 ) % minind(1)==1
          labB = 3;
      else
          if classvec(1)<0
              labB = 2;
          else
              labB = 1;
          end
      end
  end
      
end